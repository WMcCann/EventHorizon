USE EVENTHORIZON_PROD
go

/*
	-- consulta - posts do facebook 

*/


SELECT	CRBD.name as 'NomeCliente'
	,	FACE.name as 'RedeSocial'
	,	MSFM.facebook_id
	,	MSFM.author_facebook_id
	,	FACE.link
	,	REPLACE(REPLACE(REPLACE(MSFM.[Message], CHAR(9),' '), CHAR(10), ' '), CHAR(13), ' ') AS message
	,	MSFM.created_time
	,	MSFM.message_type
	,	MSFM.likes  
	,	MSFM.shares
	,	MSFM.comments
  FROM	dbo.CORE_ADVERTISER as CADV with (NOLOCK)
 INNER	JOIN dbo.CORE_BRAND as CRBD with (NOLOCK)
	ON	CADV.id = CRBD.advertiser_id
 INNER	JOIN dbo.SOCIAL_BRANDFACEBOOKPAGE as BRFB with (NOLOCK)
	ON	BRFB.brand_id = CRBD.id
 INNER	JOIN dbo.SOCIAL_FACEBOOKPAGE as FACE with (NOLOCK)
	ON	FACE.id = BRFB.facebookpage_ptr_id
 INNER	JOIN dbo.METRICS_SOCIAL_FACEBOOKMESSAGE as MSFM with (NOLOCK)
	ON	MSFM.facebook_page_id = FACE.id
 WHERE	CRBD.category_id = 314			/* 314 = VECULOS PASSEIO */
   AND	CADV.mnemonic = 'GM'
   AND	MSFM.created_time >= DATEADD( day, -3, GETDATE() )
 ORDER BY CRBD.name
	,	FACE.name
	,	MSFM.created_time DESC
		

go

-------------------------------------------------------------------------------------------------------------------------------
/*

	-- consulta - comentários dos posts do facebook  (metrics_social_facebookcomment)

*/

SELECT	CRBD.name as 'NomeCliente'
	,	MSFM.facebook_id
	,	MSFC.author_facebook_id
	,	MSFC.message_id
	,	REPLACE(REPLACE(REPLACE(MSFC.comment, CHAR(9),' '), CHAR(10), ' '), CHAR(13), ' ') AS comment
	,	MSFC.created_time
	,	MSFC.likes  
  FROM	dbo.CORE_ADVERTISER as CADV with (NOLOCK)
 INNER	JOIN dbo.CORE_BRAND as CRBD with (NOLOCK)
	ON	CADV.id = CRBD.advertiser_id
 INNER	JOIN dbo.SOCIAL_BRANDFACEBOOKPAGE as BRFB with (NOLOCK)
	ON	BRFB.brand_id = CRBD.id
 INNER	JOIN dbo.SOCIAL_FACEBOOKPAGE as FACE with (NOLOCK)
	ON	FACE.id = BRFB.facebookpage_ptr_id
 INNER	JOIN dbo.METRICS_SOCIAL_FACEBOOKMESSAGE as MSFM with (NOLOCK)
	ON	MSFM.facebook_page_id = FACE.id
 INNER	JOIN dbo.METRICS_SOCIAL_FACEBOOKCOMMENT as MSFC with (NOLOCK)
	ON	MSFM.id	= MSFC.message_id
 WHERE	CRBD.category_id = 314			/* 314 = VECULOS PASSEIO */
   AND	CADV.mnemonic = 'GM'
   AND	MSFM.created_time >= DATEADD( day, -3, GETDATE() )
 ORDER BY CRBD.name
	,	MSFM.created_time DESC
	,	MSFC.created_time DESC

go