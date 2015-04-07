USE EVENTHORIZON_PROD
go

/* ABA "fb-PageDataSource" */

WITH SELECT_BASE AS
    (   SELECT  'link' = FACE.link 
            ,   'facebook_id' = MSFM.facebook_id
            ,   'message' = REPLACE(REPLACE(REPLACE(MSFM.[message], CHAR(9),' '), CHAR(10), ' '), CHAR(13), ' ')
            ,   'Date' = CAST( MSFM.created_time as date )
            ,   'Time' = CAST( MSFM.created_time as time )
            ,   'dimension' = CASE WHEN ( MSIM.dimension IS NULL AND MSIM.metric = 'post_impressions_unique' ) THEN 'reach' ELSE MSIM.dimension END
            ,   'value' = ISNULL( MSIM.value , 0 )
            --, 'created_time' = MSFM.created_time
            --, 'metric' = MSIM.metric
            --, 'period' = MSIM.period
            --, MSFM.likes
            --, MSFM.comments   
            --, MSFM.shares
          FROM  dbo.CORE_BRAND as CRBD with (NOLOCK)
         INNER  JOIN dbo.SOCIAL_BRANDFACEBOOKPAGE as BRFB with (NOLOCK)
            ON  BRFB.brand_id = CRBD.id
         INNER  JOIN dbo.SOCIAL_FACEBOOKPAGE as FACE with (NOLOCK)
            ON  FACE.id = BRFB.facebookpage_ptr_id
         INNER  JOIN dbo.METRICS_SOCIAL_FACEBOOKMESSAGE as MSFM with (NOLOCK)
            ON  MSFM.facebook_page_id = FACE.id
         INNER  JOIN dbo.METRICS_SOCIAL_INSIGHTSMETRIC as MSIM with (NOLOCK)
            ON  MSIM.facebook_message_id = MSFM.id
         WHERE  CRBD.category_id = 314          /* 314 = VEICULOS PASSEIO */
           AND  MSFM.created_time BETWEEN '20130901' and '20130930 23:59:59'
           AND  MSIM.period = 'lifetime'
           AND  (   ( MSIM.metric IN ( 'post_consumptions_by_type', 'post_negative_feedback_by_type',/*'post_consumptions_by_type_unique', 'post_negative_feedback_by_type_unique', */ 'post_stories_by_action_type' )
                     AND    MSIM.dimension IN ( 'hide_clicks', 'xbutton_clicks', 'report_spam_clicks', 'unlike_page_clicks','photo view','video play','other clicks','link clicks', 'like', 'share', 'comment' ) )
                OR  ( MSIM.metric = 'post_impressions_unique' AND MSIM.dimension IS NULL )  /* REACH >>> NULL é válido apenas "post_impressions_unique" ... */
                )
    )
 SELECT link 
    ,   facebook_id
    ,   [message]
    ,   [date]
    ,   [time]
    ,   'like'              = ISNULL( P.[like], 0 )
    ,   'comment'           = ISNULL( P.comment, 0 )
    ,   'share'             = ISNULL( P.share, 0 )
    ,   'reach'             = ISNULL( P.reach, 0 )
    ,   'hide_clicks'       = ISNULL( P.hide_clicks, 0 )
    ,   'xbutton_clicks'    = ISNULL( P.xbutton_clicks, 0 )
    ,   'report_spam_clicks'= ISNULL( P.report_spam_clicks, 0 )
    ,   'unlike_page_clicks'= ISNULL( P.unlike_page_clicks, 0 )
    ,   'photo view'        = ISNULL( P.[photo view], 0 )
    ,   'video play'        = ISNULL( P.[video play], 0 )
    ,   'other clicks'      = ISNULL( P.[other clicks], 0 )
    ,   'link clicks'       = ISNULL( P.[link clicks], 0 )
   FROM SELECT_BASE 
  PIVOT ( SUM(value) FOR dimension IN ( [reach], [hide_clicks], [xbutton_clicks], [report_spam_clicks], [unlike_page_clicks],[photo view],[video play],[other clicks],[link clicks], [like], [share], [comment] ) ) P;

go