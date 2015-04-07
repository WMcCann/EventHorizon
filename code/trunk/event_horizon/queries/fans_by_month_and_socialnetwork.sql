DECLARE @brand        int
    ,   @brand_name   nvarchar(510)
    ,   @dtini        datetime
    ,   @dtfim        datetime
    ,   @total        int
/* Sum of values with MAX date from last day of the month */


SELECT  @brand = %s
    ,   @brand_name = '%s'
    ,   @dtini = '%s'
    ,   @dtfim = '%s'
    ,   @total = 0 ;

/* 2 > Query returns growth evolution of last XX months ... */

-- FACEBOOK
    
SELECT  'ORIGIN' = 'FACEBOOK'
    ,   'BRAND' = @brand_name
    ,   X.ANO
    ,   X.MES
    ,   'TOTAL'  =  MSFP.likes
  FROM  dbo.METRICS_SOCIAL_EVOLUTIONFACEBOOKPAGELIKE as MSFP with (NOLOCK)
 INNER  JOIN (  SELECT  MSEL.facebook_page_id
                    ,   'ANO'  = YEAR( MSEL.[date]) 
                    ,   'MES'  = MONTH( MSEL.[date]) 
                    ,   'Data' = MAX( MSEL.[date])
                  FROM  dbo.CORE_ADVERTISER as CADV with (NOLOCK)
                 INNER  JOIN dbo.CORE_BRAND as CRBD with (NOLOCK)
                    ON  CADV.id = CRBD.advertiser_id
                 INNER  JOIN dbo.SOCIAL_BRANDFACEBOOKPAGE as BRFB with (NOLOCK)
                    ON  BRFB.brand_id = CRBD.id
                 INNER  JOIN dbo.SOCIAL_FACEBOOKPAGE as FACE with (NOLOCK)
                    ON  FACE.id = BRFB.facebookpage_ptr_id
                 INNER  JOIN dbo.METRICS_SOCIAL_EVOLUTIONFACEBOOKPAGELIKE as MSEL with (NOLOCK)
                    ON  MSEL.facebook_page_id = FACE.id
                 WHERE  CRBD.id = @brand
                   AND  CAST( MSEL.[date] as [date] ) BETWEEN @dtini AND @dtfim
                 GROUP  BY MSEL.facebook_page_id, YEAR( MSEL.[date]) , MONTH( MSEL.[date])
                ) as  X
    ON  MSFP.[date] = X.Data
   AND  MSFP.facebook_page_id = X.facebook_page_id 

UNION ALL 

    /* TWITTER */
    SELECT  'ORIGIN' = 'TWITTER'
        ,   'BRAND' = @brand_name
        ,   X.ANO
        ,   X.MES
        ,   'TOTAL'  =  MSTW.followers_count
      FROM  dbo.metrics_social_evolutiontwitterprofile as MSTW with (NOLOCK)
     INNER  JOIN (  SELECT  MSEL.twitter_profile_id
                        ,   'ANO'  = YEAR( MSEL.[date]) 
                        ,   'MES'  = MONTH( MSEL.[date]) 
                        ,   'Data' = MAX( MSEL.[date])
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
                       AND  CAST( MSEL.[date] as [date] ) = @dtfim  
                     GROUP  BY MSEL.twitter_profile_id, YEAR( MSEL.[date]) , MONTH( MSEL.[date])
                ) AS X
    ON  MSTW.[date] = X.Data
   AND  MSTW.twitter_profile_id = X.twitter_profile_id 

UNION ALL

    /* YOUTUBE */
    SELECT  'ORIGIN' = 'YOUTUBE'
        ,   'BRAND' = @brand_name
        ,   X.ANO
        ,   X.MES
        ,   'TOTAL'  =  MSTW.subscribers_count
      FROM  dbo.metrics_social_evolutionyoutubechannel as MSTW with (NOLOCK)
     INNER  JOIN (  SELECT  MSEL.youtube_channel_id
                        ,   'ANO'  = YEAR( MSEL.[date]) 
                        ,   'MES'  = MONTH( MSEL.[date]) 
                        ,   'Data' = MAX( MSEL.[date])
                      FROM  dbo.CORE_ADVERTISER as CADV with (NOLOCK)
                     INNER  JOIN dbo.CORE_BRAND as CRBD with (NOLOCK)
                        ON  CADV.id = CRBD.advertiser_id
                     INNER  JOIN dbo.social_brandyoutubechannel as BRTW with (NOLOCK)
                        ON  BRTW.brand_id = CRBD.id
                     INNER  JOIN dbo.social_youtubechannel as TWIT with (NOLOCK)
                        ON  TWIT.id = BRTW.youtubechannel_ptr_id
                     INNER  JOIN dbo.metrics_social_evolutionyoutubechannel as MSEL with (NOLOCK)
                        ON  MSEL.youtube_channel_id = TWIT.id
                     WHERE  CRBD.id = @brand
                       AND  CAST( MSEL.[date] as [date] ) = @dtfim  
                     GROUP  BY  MSEL.youtube_channel_id, YEAR( MSEL.[date]) , MONTH( MSEL.[date])
                ) AS X
        ON  MSTW.[date] = X.Data
       AND  MSTW.youtube_channel_id = X.youtube_channel_id 
 ORDER  BY ORIGIN, ANO desc, mes ;