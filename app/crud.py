from typing import Optional, List
from .models.user import User
from .models.user_client import UserClient
from .models.company import Company
from .models.client import Client
from .models.article import Article
from .models.client_article import ClientArticle
from .database.connection import create_connection


def get_user(loginname: str) -> Optional[User]:
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM usermaster WHERE LOGINNAME = :loginname", {"loginname": loginname})
        user_data = cursor.fetchone()

        if user_data:
            column_names = [desc[0] for desc in cursor.description]
            return dict(zip(column_names, user_data))
        else:
            return None


def get_clients() -> List[Client]:
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT clientid, clientname FROM clientmaster WHERE ISACTIVE = 'Y' ORDER BY clientname")
        user_data = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        clients = []
        for row in user_data:
            row_dict = dict(zip(column_names, row))
            clients.append(row_dict)

        return clients


def get_companies(client_id: str) -> List[Company]:
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT cb.clientid, cm.companyid, cm.companyname
            FROM companymaster cm, clientbasket cb
            WHERE cb.companyid = cm.companyid AND cm.isactive = 'Y'
            AND cb.clientid = :client_id
            ORDER BY cm.companyname
        """, {"client_id": client_id})

        companies = [Company(clientid=row[0], companyid=row[1],
                             companyname=row[2]) for row in cursor.fetchall()]

    return companies


def get_user_clients(loginname: str) -> List[UserClient]:
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT UM.LOGINNAME, UCD.CLIENTID, CM.CLIENTNAME
            FROM CIRRUS.USERMASTER UM
            JOIN CIRRUS.USERCLIENTDETAIL UCD ON UM.USERSID = UCD.USERSID
            JOIN CIRRUS.CLIENTMASTER CM ON UCD.CLIENTID = CM.CLIENTID
            WHERE UM.LOGINNAME LIKE :loginname
        """, {"loginname": f"%{loginname}%"})

        user_clients = [UserClient(
            loginname=row[0], clientid=row[1], clientname=row[2]) for row in cursor.fetchall()]

    return user_clients


def get_articles() -> List[Article]:
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT *
            FROM (
                SELECT DISTINCT cm.companyname, LINK, ah.socialfeedid, TO_CHAR(feeddate, 'Mon dd,yy'),
                    CASE NVL(cah.headlines, '0')
                        WHEN '0' THEN funcsplchar1(ah.headline_snippet)
                        ELSE funcsplchar1(cah.headlines)
                    END headlines,
                    ah.publication, ah.publicationid, funcsplchar1(NVL(SUMMARY_SNIPPET, '-')) summary_snippet,
                    emailpriority, NULL feeddate, ad.companyid, '' tone, reach, engagement, articledatenumber
                FROM SOCIALFEEDHEADER ah, socialfeeddetail ad, companymaster cm, clientbasket cb, clientarticleheader cah
                WHERE NVL(ah.isactive, 'Y') = 'Y'
                    AND ah.articledatenumber >= TO_NUMBER(TO_CHAR(TO_DATE('01/12/2023', 'dd/mm/yyyy'), 'yyyymmdd'))
                    AND ah.articledatenumber <= TO_NUMBER(TO_CHAR(TO_DATE('01/12/2023', 'dd/mm/yyyy'), 'yyyymmdd'))
                    AND ah.socialfeedid IN (
                        SELECT s.SOCIALFEEDID
                        FROM SOCIALFEEDDATEWISE s
                        WHERE s.FEEDDATENUMBER >= TO_NUMBER(TO_CHAR(TO_DATE('01/12/2023', 'dd/mm/yyyy'), 'yyyymmdd'))
                            AND s.FEEDDATENUMBER <= TO_NUMBER(TO_CHAR(TO_DATE('01/12/2023', 'dd/mm/yyyy'), 'yyyymmdd'))
                    )
                    AND ad.companyid IN ('136', 'IKA', 'ATCINDO')
                    AND ah.socialfeedid = ad.socialfeedid
                    AND ad.companyid = cm.companyid
                    AND cb.companyid = ad.companyid
                    AND cb.clientid = 'AS'
                    AND cah.clientid(+) = 'AS'
                    AND ah.socialfeedid = cah.articleid(+)
                    AND NVL(cb.isactive, 'Y') = 'Y'
                    AND NVL(cm.isactive, 'Y') = 'Y'
                    AND ah.publicationid IN (SELECT publicationid FROM onlinepublicationmaster_QC)
                    AND (ah.socialfeedid, ad.companyid) NOT IN (
                        SELECT DISTINCT articleid, companyid
                        FROM articletagonline
                        WHERE clientid = 'AS' AND tag = '<----Deleted---->'
                    )
            )
            ORDER BY articledatenumber DESC
        """)

        articles = [Article(
            companyname=row[0],
            link=row[1],
            socialfeedid=row[2],
            feeddate=row[3],
            headlines=row[4],
            publication=row[5],
            publicationid=row[6],
            summary_snippet=row[7],
            emailpriority=row[8],
            companyid=row[9],
            tone=row[10],
            reach=row[11],
            engagement=row[12],
            articledatenumber=row[13]
        ) for row in cursor.fetchall()]
        return articles


def get_client_articles() -> List[ClientArticle]:
    with create_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT
                cb.clientid,
                ad.companyid,
                companyname,
                CASE nvl(
                    funcsplchar1(
                        cah.headlines
                    ), '0'
                )
                WHEN '0' THEN
                funcsplchar1(
                    ah.headlines
                )
                ELSE
                funcsplchar1(
                    cah.headlines
                )
                END     headlines,
                ah.publicationname,
                ah.articleid,
                to_char(
                    ah.articledate, 'Month dd yyyy'
                )       articledate,
                getcity(
                    ah.articleid
                )       uploadcity,
                nvl(
                    ah.journalist, '-'
                ),
                get_pagenos(
                    ah.articleid
                ),
                to_number(
                    decode(
                        nvl(
                            emailpriority, 1000
                        ), 0, 1000, nvl(
                            emailpriority, 1000
                        )
                    )
                )       emailpriority,
                nvl(
                    haspdf, 'N'
                )       haspdf,
                nvl(
                    hashtml, 'N'
                )       hashtml,
                nvl(
                    funcsplchar1(
                        ah.articlesummary
                    ), '-'
                )       articlesummary,
                nvl(
                    ah.space, 0
                )       space,
                pubgroupname,
                pubcategory,
                nvl(
                    c.hassummary, 'Y'
                ),
                nvl(
                    height, 0
                )       height,
                nvl(
                    width, 0
                ),
                nvl(
                    cb.mailsectionid, 0
                )       width,
                getarticledetailtextorgone(
                    ah.articleid
                ),
                'dummy' artstate,
                initcap(
                    pm.language
                ),
                nvl(
                    getclientarticletags(
                        ah.articleid, 'AS', ad.companyid
                    ), '-'
                ),
                nvl(
                    cat.tone, 0
                ),
                nvl(
                    ad.sortorder, 999
                )       priority,
                getclubarticle(
                    ah.articleid, cb.clientid
                )       otherpubs
            FROM
                articleheader           ah,
                clientarticleheader     cah,
                articledetail           ad,
                clientbasket            cb,
                companymaster           cm,
                clientmaster            c,
                publicationmaster       pm,
                publicationgroupmaster  pgm,
                citymaster              city,
                clientarticletonedetail cat
            WHERE
                ah.articleid = ad.articleid
                AND ah.articleid = cah.articleid (+)
                AND ad.articleid = cat.articleid (+)
                AND ad.companyid = cat.companyid (+)
                AND ad.companyid = cb.companyid
                AND ad.companyid = cm.companyid
                AND cb.clientid = c.clientid
                AND city.cityid = ah.cityid
                AND ah.publicationid = pm.publicationid
                AND pgm.pubgroupid = ah.pubgroupid
                AND nvl(
                    c.mailerlogic, 'C'
                ) = 'H'
                AND nvl(
                    ah.isactive, 'Y'
                ) = 'Y'
                AND nvl(
                    cb.isactive, 'Y'
                ) != 'N'
                AND nvl(
                    c.isactive, 'Y'
                ) != 'N'
                AND nvl(
                    cm.isactive, 'Y'
                ) != 'N'
                AND cb.clientid = 'AS'
                AND cat.clientid (+) = 'AS'
                AND cah.clientid (+) = 'AS'
                AND EXISTS (
                    SELECT
                        1
                    FROM
                        clientmailarticles x
                    WHERE
                        x.articleid = ah.articleid
                        AND x.articleid NOT IN (
                            SELECT
                                adc.articleid
                            FROM
                                articledetailcopy  adc, clientmailarticles cm
                            WHERE
                                mainarticleid = cm.articleid
                            UNION ALL
                            SELECT
                                adc.articleid
                            FROM
                                articledetailcopyqc adc, clientmailarticles  cm
                            WHERE
                                mainarticleid = cm.articleid
                                AND ( ah.articleid, ad.companyid ) NOT IN (
                                    SELECT DISTINCT
                                        articleid, companyid
                                    FROM
                                        articletagdetail atd
                                    WHERE
                                        clientid = 'AS'
                                        AND tag = '<----Deleted---->'
                                )
                            UNION ALL
                            SELECT
                                adc.articleid
                            FROM
                                articleclubdetail  adc, clientmailarticles cm
                            WHERE
                                adc.clientid = 'AS'
                                AND mainarticleid <> adc.articleid
                                AND mainarticleid = cm.articleid
                        )
                )
                AND ad.articleid IN (
                    SELECT DISTINCT
                        articleid
                    FROM
                        articledetail
                    WHERE
                        articleid IN (
                            SELECT
                                articleid
                            FROM
                                clientmailarticles
                        )
                        AND companyid IN ( '136' )
                )
            ORDER BY
                clientid,
                to_number(
                    replace(
                        emailpriority, 0, 1000
                    )
                ),
                ah.articledate DESC,
                priority,
                priority_level1,
                priority_level2,
                priority_level3
        """)

        articles = [ClientArticle(
            clientid=row[0],
            companyid=row[1],
            companyname=row[2],
            headlines=row[3],
            publicationname=row[4],
            articleid=row[5],
            articledate=row[6],
            uploadcity=row[7],
            journalist=row[8],
            pagenos=row[9],
            emailpriority=row[10],
            haspdf=row[11],
            hashtml=row[12],
            articlesummary=row[13],
            space=row[14],
            pubgroupname=row[15],
            pubcategory=row[16],
            hassummary=row[17],
            height=row[18],
            width=row[19],
            mailsectionid=row[20],
            articledetailtextorgone=row[21],
            artstate=row[22],
            language=row[23],
            tags=row[24],
            tone=row[25],
            priority=row[26],
            otherpubs=row[27]
        ) for row in cursor.fetchall()]

    return articles
