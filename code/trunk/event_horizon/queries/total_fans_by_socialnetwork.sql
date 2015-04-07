DECLARE @brand        int
    ,   @brand_name   nvarchar(510)
    ,   @dtini        datetime
    ,   @dtfim        datetime

/* Sum of values with MAX date from last day of the month */

SELECT  @brand = %s
    ,   @brand_name = '%s'
    ,   @dtini = '%s'
    ,   @dtfim = '%s';

WITH SELECT_BASE (ORIGEM, BRAND, TOTAL) AS 
(
    /* FACEBOOK */
    SELECT  'ORIGIN' = 'FACEBOOK'
        ,   'BRAND'  = @brand_name
        ,   'TOTAL'  =  ISNULL((SELECT   SUM( MSFP.likes)
                                  FROM  dbo.METRICS_SOCIAL_EVOLUTIONFACEBOOKPAGELIKE as MSFP with (NOLOCK)
                                 INNER   JOIN (      SELECT  MSEL.facebook_page_id, MAX(MSEL.[date]) as 'data'
                                                  FROM  dbo.CORE_ADVERTISER as CADV with (NOLOCK)
                                                 INNER  JOIN dbo.CORE_BRAND as CRBD with (NOLOCK)
                                                    ON  CADV.id = CRBD.advertiser_id
                                                 INNER  JOIN dbo.SOCIAL_BRANDFACEBOOKPAGE as BRFB with (NOLOCK)
                                                    ON  BRFB.brand_id = CRBD.id
                                                 INNER  JOIN dbo.SOCIAL_FACEBOOKPAGE as FACE with (NOLOCK)
                                                    ON  FACE.id = BRFB.facebookpage_ptr_id
                                                 INNER  JOIN dbo.METRICS_SOCIAL_EVOLUTIONFACEBOOKPAGELIKE as MSEL with (NOLOCK)
                                                    ON  MSEL.facebook_page_id = FACE.id
                                                 WHERE     CRBD.id = @brand
                                                   AND  CAST( MSEL.[date] as [date] ) BETWEEN @dtini AND @dtfim
                                                 GROUP     BY MSEL.facebook_page_id
                                              ) as X
                                                     ON    MSFP.facebook_page_id = X.facebook_page_id
                                                  AND      MSFP.[date] = X.data
                                ), 0)



    UNION ALL

    /* TWITTER */
    SELECT  'ORIGIN' = 'TWITTER'
        ,   'BRAND'  = @brand_name
        ,   'TOTAL'  =  ISNULL((SELECT   SUM( MSTW.followers_count )
                                  FROM  dbo.metrics_social_evolutiontwitterprofile as MSTW with (NOLOCK)
                                 INNER   JOIN (      SELECT  MSEL.twitter_profile_id , MAX(MSEL.[date]) as 'data'
                                                                         FROM  dbo.CORE_ADVERTISER as CADV with (NOLOCK)
                                                                       INNER  JOIN dbo.CORE_BRAND as CRBD with (NOLOCK)
                                                                            ON  CADV.id = CRBD.advertiser_id
                                                                       INNER  JOIN dbo.SOCIAL_BRANDTWITTERPROFILE as BRTW with (NOLOCK)
                                                                            ON  BRTW.brand_id = CRBD.id
                                                                       INNER  JOIN dbo.social_twitterprofile as TWIT with (NOLOCK)
                                                                            ON  TWIT.id = BRTW.twitterprofile_ptr_id
                                                                       INNER  JOIN dbo.METRICS_SOCIAL_EVOLUTIONTWITTERPROFILE as MSEL with (NOLOCK)
                                                                            ON  MSEL.twitter_profile_id = TWIT.id
                                                                       WHERE  CRBD.id = @brand
                                                                          AND  CAST( MSEL.[date] as [date] ) BETWEEN @dtini AND @dtfim
                                                                       GROUP      BY MSEL.twitter_profile_id
                                                                       ) as X
                                                     ON    X.twitter_profile_id = MSTW.twitter_profile_id
                                                  AND  MSTW.[date] = X.data
                                ), 0)

    UNION ALL

    /* YOUTUBE */
    SELECT  'ORIGIN' = 'YOUTUBE'
        ,   'BRAND'  = @brand_name
        ,   'TOTAL'  =  ISNULL((SELECT   SUM( MSYC.subscribers_count )
                                  FROM  dbo.metrics_social_evolutionyoutubechannel as MSYC with (NOLOCK)
                                 INNER   JOIN (      SELECT  MSEL.youtube_channel_id , MAX(MSEL.[date]) as 'data'
                                                  FROM  dbo.CORE_ADVERTISER as CADV with (NOLOCK)
                                                 INNER  JOIN dbo.CORE_BRAND as CRBD with (NOLOCK)
                                                    ON  CADV.id = CRBD.advertiser_id
                                                 INNER  JOIN dbo.social_brandyoutubechannel as BRYC with (NOLOCK)
                                                    ON  BRYC.brand_id = CRBD.id
                                                 INNER  JOIN dbo.social_youtubechannel as TWIT with (NOLOCK)
                                                    ON  TWIT.id = BRYC.youtubechannel_ptr_id
                                                 INNER  JOIN dbo.metrics_social_evolutionyoutubechannel as MSEL with (NOLOCK)
                                                    ON  MSEL.youtube_channel_id = TWIT.id
                                                 WHERE  CRBD.id = @brand
                                                   AND  CAST( MSEL.[date] as [date] ) BETWEEN @dtini AND @dtfim
                                                 GROUP     BY MSEL.youtube_channel_id
                                                ) as X
                                                     ON    X.youtube_channel_id = MSYC.youtube_channel_id
                                                  AND  X.data = MSYC.[date]
                                ), 0)
)

/* This query returns splited values */
SELECT * FROM SELECT_BASE