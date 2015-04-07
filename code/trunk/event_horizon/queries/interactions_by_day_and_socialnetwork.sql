-- Method:
-- Sum interactions group by day, month and year (Last 6 months)

DECLARE @brand int
    ,   @brand_name  nvarchar(510)
    ,   @dtini  datetime
    ,   @dtfim  datetime

SELECT  @brand = %s
    ,   @brand_name = '%s'
    ,   @dtini = '%s'
    ,   @dtfim = '%s';

/* 3 > returns last 30 days interactions by socialnetwork ... */
WITH SELECT_BASE AS
    (   -- FACEBOOK
        SELECT  'ORIGIN' = 'FACEBOOK'
            ,   'BRAND'  = @brand_name
            ,   'YEAR'   = YEAR( MSFM.created_time )
            ,   'MONTH'  = MONTH( MSFM.created_time )
            ,   'DAY'    = DAY( MSFM.created_time )
            ,   'TOTAL'  = SUM( MSFM.likes + MSFM.shares + MSFM.comments )
          FROM  dbo.CORE_ADVERTISER as CADV with (NOLOCK)
         INNER  JOIN dbo.CORE_BRAND as CRBD with (NOLOCK)
            ON  CADV.id = CRBD.advertiser_id
         INNER  JOIN dbo.SOCIAL_BRANDFACEBOOKPAGE as BRFB with (NOLOCK)
            ON  BRFB.brand_id = CRBD.id
         INNER  JOIN dbo.SOCIAL_FACEBOOKPAGE as FACE with (NOLOCK)
            ON  FACE.id = BRFB.facebookpage_ptr_id
         INNER  JOIN dbo.METRICS_SOCIAL_FACEBOOKMESSAGE as MSFM with (NOLOCK)
            ON  MSFM.facebook_page_id = FACE.id
         WHERE  CRBD.id = @brand
           AND  CAST( MSFM.created_time as [date]) BETWEEN @dtini AND @dtfim
         GROUP  BY YEAR( MSFM.created_time )
            ,   MONTH( MSFM.created_time )
            ,   DAY( MSFM.created_time )

    UNION ALL
    
        -- TWITTER
        SELECT  'ORIGIN' = 'TWITTER'
            ,   'BRAND'  = @brand_name
            ,   'YEAR'   = YEAR( MSTM.created_time )
            ,   'MONTH'  = MONTH( MSTM.created_time )
            ,   'DAY'    = DAY( MSTM.created_time )
            ,   'TOTAL'  = SUM( MSTM.favorites + MSTM.retweets )
          FROM  dbo.CORE_ADVERTISER as CADV with (NOLOCK)
         INNER  JOIN dbo.CORE_BRAND as CRBD with (NOLOCK)
            ON  CADV.id = CRBD.advertiser_id
         INNER  JOIN dbo.SOCIAL_BRANDTWITTERPROFILE as BRTP with (NOLOCK)
            ON  BRTP.brand_id = CRBD.id
         INNER  JOIN dbo.SOCIAL_TWITTERPROFILE as TWIT with (NOLOCK)
            ON  TWIT.id = BRTP.twitterprofile_ptr_id
         INNER  JOIN dbo.METRICS_SOCIAL_TWITTERMESSAGE as MSTM with (NOLOCK)
            ON  MSTM.twitter_profile_id = TWIT.id
         WHERE  CRBD.id = @brand
           AND  CAST( MSTM.created_time as [date]) BETWEEN @dtini AND @dtfim
         GROUP  BY YEAR( MSTM.created_time )
            ,   MONTH( MSTM.created_time )
            ,   DAY( MSTM.created_time )
    UNION ALL
        -- YOUTUBE
        SELECT  'ORIGIN' = 'YOUTUBE'
            ,   'BRAND'  = @brand_name
            ,   'YEAR'   = YEAR( MSYV.created_time )
            ,   'MONTH'  = MONTH( MSYV.created_time )
            ,   'DAY'    = DAY( MSYV.created_time )
            ,   'TOTAL'  = SUM( MSYV.likes + MSYV.comments + MSYV.favorites )
          FROM  dbo.CORE_ADVERTISER as CADV with (NOLOCK)
         INNER  JOIN dbo.CORE_BRAND as CRBD with (NOLOCK)
            ON  CADV.id = CRBD.advertiser_id
         INNER  JOIN dbo.SOCIAL_BRANDYOUTUBECHANNEL as BRYC with (NOLOCK)
            ON  BRYC.brand_id = CRBD.id
         INNER  JOIN dbo.SOCIAL_YOUTUBECHANNEL as YUTB with (NOLOCK)
            ON  YUTB.id = BRYC.youtubechannel_ptr_id
         INNER  JOIN dbo.metrics_social_youtubevideo as MSYV with (NOLOCK)
            ON  MSYV.youtube_channel_id = YUTB.id
         WHERE  CRBD.id = @brand
           AND  CAST( MSYV.created_time as [date]) BETWEEN @dtini AND @dtfim
         GROUP  BY YEAR( MSYV.created_time )
            ,   MONTH( MSYV.created_time )
            ,   DAY( MSYV.created_time )
    )
SELECT  BRAND
    ,   YEAR
    ,   MONTH
    ,   DAY
    ,   'FACEBOOK'  = ISNULL( P.FACEBOOK, 0)
    ,   'TWITTER'   = ISNULL( P.TWITTER , 0)
    ,   'YOUTUBE'   = ISNULL( P.YOUTUBE , 0)
 FROM SELECT_BASE 
  PIVOT ( SUM(Total) FOR ORIGIN IN ( [FACEBOOK], [TWITTER] , [YOUTUBE] ) ) P
 ORDER BY YEAR desc, MONTH desc, DAY desc;