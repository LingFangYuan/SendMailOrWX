SELECT DT 日期,
       UV,
       PV,
       TO_CHAR(ROUND((UV - YD_UV) / YD_UV, 4)*100,'FM990.90') || '%' as UV环比,
       TO_CHAR(ROUND((PV - YD_PV) / YD_PV, 4)*100,'FM990.90') || '%' as PV环比,
       UV_AVG 平均UV,
       PV_AVG 平均PV,
       
       CASE
         WHEN UV > 2.5 * UV_AVG OR PV > 4 * PV_AVG OR
              ABS((UV - YD_UV) / YD_UV) > 2.5 OR ABS((PV - YD_PV) / YD_PV) > 2.5 THEN
          1
         ELSE
          0
       END FLAG
  FROM (SELECT DT,
               UV,
               PV,
               LAG(UV, 1) OVER(ORDER BY DT) YD_UV,
               LAG(PV, 1) OVER(ORDER BY DT) YD_PV,
               ROUND(AVG(UV) OVER(), 0) UV_AVG,
               ROUND(AVG(PV) OVER(), 0) PV_AVG
          FROM DW_FLOWS_LOG_MAIDIAN_DAY
         WHERE DT > (SYSDATE - 61)
           AND USER_TYPE IS NULL
           AND TARGET_TYPE IS NULL
           AND EVENT_ID IS NULL)
 WHERE DT >= TRUNC(SYSDATE - 7) 
 ORDER BY DT DESC
