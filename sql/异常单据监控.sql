
select REMARK 异常类型, COUNT(1) 异常数量 from (
#1.返利日志表，已经支付的订单，到期日期异常：
#1. 商品：到期日期-支付日期-1>订单自动确认收货时间+商品退货期限；
#2. 大礼包：到期日期-支付日期-1>订单自动确认收货时间+大礼包退货期限；
SELECT '支付的订单-到期日期异常' REMARK,
	ORDER_NUMBER,
	ORDER_PAY_DATE,
	out_time_end_date,
	order_type,
	state_buss 
FROM
	(
	SELECT
		a.ORDER_NUMBER,
		ORDER_PAY_DATE,
		B.out_time_end_date,
	CASE
			
			WHEN b.order_type = 1 THEN
			'大礼包' ELSE '普通商品' 
		END order_type,
CASE
		
		WHEN b.order_type = 1 THEN
		10+0 ELSE 10+7 
	END set_days,
	DATEDIFF( out_time_end_date, ORDER_PAY_DATE ) Actual_days,
CASE
		b.state_buss 
		WHEN 1 THEN
		'未转正' 
		WHEN 2 THEN
		'已退款' 
		WHEN 3 THEN
		'已转正' 
	END AS state_buss 
FROM
	blc_order A
	JOIN roma_customer_order_item_log B ON A.ORDER_ID = B.ORDER_ID 
WHERE
	1 = 1 
	AND ORDER_PAY_DATE >= date_sub( curdate( ), INTERVAL 30 DAY ) 
	AND a.ORDER_STATUS = 'COMPLETED' 
	AND out_time_end_date < curdate( ) ) c WHERE Actual_days > set_days 


UNION ALL 	  
#2.订单的商品已经取消成功，但是返利日志表，该商品的返利状态没回滚；
SELECT '已退单-返利状态不为退单' REMARK,
	c.ORDER_NUMBER,
	c.ORDER_PAY_DATE,
	out_time_end_date,
CASE
		b.order_type 
		WHEN 1 THEN
		'大礼包 ' 
		WHEN 2 THEN
		'普通订单' 
	END order_type,
CASE
		b.state_buss 
		WHEN 1 THEN
		'未转正' 
		WHEN 2 THEN
		'已退款' 
		WHEN 3 THEN
		'已转正' 
	END AS state_buss 
FROM
	roma_order_apply a
	JOIN roma_customer_order_item_log b ON a.ORDER_ITEM_ID = b.ORDER_ITEM_ID 
	AND state_buss <> 2 
	AND out_time_end_date < curdate( )
	JOIN blc_order c ON a.order_id = c.order_id 
WHERE
	apply_status = 'COMPLETED' 


UNION ALL 	
#3.订单已经支付成功，但是返利日志表没数据；
SELECT
	'已经订单-无返利日志' REMARK,
	ORDER_NUMBER,
	ORDER_PAY_DATE,
	out_time_end_date,
	order_type,
	state_buss 
FROM
	(
	SELECT
		a.ORDER_NUMBER,
		a.ORDER_PAY_DATE,
		out_time_end_date,
	CASE
			b.order_type 
			WHEN 1 THEN
			'大礼包 ' 
			WHEN 2 THEN
			'普通订单' 
		END order_type,
CASE
		b.state_buss 
		WHEN 1 THEN
		'未转正' 
		WHEN 2 THEN
		'已退款' 
		WHEN 3 THEN
		'已转正' 
	END AS state_buss,
	b.order_id 
FROM
	blc_order a
	LEFT JOIN roma_customer_order_item_log b ON a.ORDER_ID = b.ORDER_ID 
WHERE
	ORDER_PAY_DATE IS NOT NULL 
	) a 
WHERE
	order_id IS NULL

UNION ALL
#4.订单正常完成，但是返利日志表状态为回滚状态。
SELECT
	'正常订单-返利状态回滚' REMARK,
	ORDER_NUMBER,
	ORDER_PAY_DATE,
	out_time_end_date,
	order_type,
	state_buss 
FROM
	(
	SELECT
		a.ORDER_NUMBER,
		a.order_id,
		a.ORDER_PAY_DATE,
		out_time_end_date,
	CASE
			b.order_type 
			WHEN 1 THEN
			'大礼包 ' 
			WHEN 2 THEN
			'普通订单' 
		END order_type,
CASE
		b.state_buss 
		WHEN 1 THEN
		'未转正' 
		WHEN 2 THEN
		'已退款' 
		WHEN 3 THEN
		'已转正' 
	END AS state_buss,
	c.id 
FROM
	blc_order a
	JOIN roma_customer_order_item_log b ON a.ORDER_ID = b.ORDER_ID
	LEFT JOIN roma_order_apply c ON a.order_id = c.order_id 
	AND c.apply_status = 'COMPLETED' 
WHERE
	a.ORDER_STATUS = 'COMPLETED' 
	AND state_buss <> 3 
	AND out_time_end_date < curdate( ) 
	) a 
WHERE
	id IS NULL
	
	
UNION ALL 	
#5.返利日志表的到期日期已经达成，但是状态没有改变。
SELECT '超截止日期-返利状态未变更',
	a.ORDER_NUMBER,
	a.ORDER_PAY_DATE,
	out_time_end_date,
CASE
		b.order_type 
		WHEN 1 THEN
		'大礼包 ' 
		WHEN 2 THEN
		'普通订单' 
	END order_type,
CASE
		b.state_buss 
		WHEN 1 THEN
		'未转正' 
		WHEN 2 THEN
		'已退款' 
		WHEN 3 THEN
		'已转正' 
	END AS state_buss 
FROM
	blc_order a
	JOIN roma_customer_order_item_log b ON a.ORDER_ID = b.ORDER_ID 
WHERE
	a.ORDER_STATUS = 'COMPLETED'   
	AND state_buss = 1 
	AND out_time_end_date < curdate( ) 
	
	
UNION ALL 	
#6.返利日志表的到期日期没有达成，但是状态已经是已返利。
SELECT '未达截止日期-返利状态已变更',
	a.ORDER_NUMBER,
	a.ORDER_PAY_DATE,
	out_time_end_date,
CASE
		b.order_type 
		WHEN 1 THEN
		'大礼包 ' 
		WHEN 2 THEN
		'普通订单' 
	END order_type,
CASE
		b.state_buss 
		WHEN 1 THEN
		'未转正' 
		WHEN 2 THEN
		'已退款' 
		WHEN 3 THEN
		'已转正' 
	END AS state_buss 
FROM
	blc_order a
	JOIN roma_customer_order_item_log b ON a.ORDER_ID = b.ORDER_ID 
WHERE
 state_buss = 3
	AND out_time_end_date > curdate( ) 
	) ERROR
GROUP BY REMARK	