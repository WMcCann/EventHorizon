-- Method:
-- Sum interactions group by type (Last 6 months)

DECLARE @brand  int
    ,   @brand_name  nvarchar(510)
    ,   @dtini  datetime
    ,   @dtfim  datetime

/* Sum of values with MAX date from last day of the month */
SELECT  @brand = %s
    ,   @brand_name = '%s'
    ,   @dtini = '%s'
    ,   @dtfim = '%s';

WITH SELECT_FACEBOOK AS
    (   -- FACEBOOK
        SELECT  'FACEBOOK_BRAND'     = @brand_name
            ,   'FACEBOOK_LIKES'    = SUM( ISNULL( MSFM.likes, 0))
            ,   'FACEBOOK_SHARES'   = SUM( ISNULL( MSFM.shares, 0))
            ,   'FACEBOOK_COMMENTS' = SUM( ISNULL( MSFM.comments, 0))
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
    )
, SELECT_TWITTER AS 
    (   -- TWITTER
        SELECT  'TWITTER_BRAND'  = @brand_name
            ,   'TWITTER_FAVORITES' = SUM( ISNULL( MSTM.favorites, 0))
            ,   'TWITTER_RETWEETS'  = SUM( ISNULL( MSTM.retweets, 0) )
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
    )
, SELECT_YOUTUBE AS
    (   -- YOUTUBE
        SELECT  'YOUTUBE_BRAND'  = @brand_name
            ,   'YOUTUBE_LIKES'  = SUM( ISNULL( MSYV.likes, 0) )
            ,   'YOUTUBE_COMMENTS'  = SUM( ISNULL( MSYV.comments, 0) )
            ,   'YOUTUBE_FAVORITES' = SUM( ISNULL( MSYV.favorites, 0) )
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
    )
SELECT  'BRAND' = FACEBOOK_Brand , 'DESCRIPTION' = 'FACEBOOK_LIKES' , 'TOTAL' = ISNULL( FACEBOOK_LIKES, 0) FROM SELECT_FACEBOOK
    UNION ALL
SELECT  FACEBOOK_Brand , 'FACEBOOK_SHARES' , ISNULL( FACEBOOK_SHARES, 0) FROM SELECT_FACEBOOK
    UNION ALL
SELECT  FACEBOOK_Brand , 'FACEBOOK_COMMENTS' , ISNULL( FACEBOOK_COMMENTS, 0) FROM SELECT_FACEBOOK
    UNION ALL
SELECT  TWITTER_Brand , 'TWITTER_FAVORITES' , ISNULL( TWITTER_FAVORITES, 0) FROM SELECT_TWITTER
    UNION ALL
SELECT  TWITTER_Brand , 'TWITTER_RETWEETS' , ISNULL( TWITTER_RETWEETS, 0) FROM SELECT_TWITTER
    UNION ALL
SELECT  YOUTUBE_Brand , 'YOUTUBE_LIKES' , ISNULL( YOUTUBE_LIKES, 0) FROM SELECT_YOUTUBE
    UNION ALL
SELECT  YOUTUBE_Brand , 'YOUTUBE_COMMENTS' , ISNULL( YOUTUBE_COMMENTS, 0) FROM SELECT_YOUTUBE
    UNION ALL
SELECT  YOUTUBE_Brand , 'YOUTUBE_FAVORITES' , ISNULL( YOUTUBE_FAVORITES, 0) FROM SELECT_YOUTUBE