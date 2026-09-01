# 01-04 wk03｜Open Data Set List

## 1. 目的

本書は、サービス紹介資料および分析PoCの適用事例検討に使用できるOpen Data / Public Dataset候補を一元化する。

以下を統合した。

1. 添付資料 `__open_data_source_ZZ_whole.md` に記載されたDataset一覧
2. `01-04_wk01` / `01-04_wk02` で既に調査していたOpen Data 8件
   - AI4I 2020 Predictive Maintenance
   - Appliances Energy Prediction
   - Bank Marketing
   - Beijing Multi-Site Air Quality
   - Gas Turbine CO and NOx Emission
   - Occupancy Detection
   - Airfoil Self-Noise
   - NASA Prognostics

重複するDatasetは原則統合し、別公開版・派生版に意味がある場合は別行として残す。

> **注意**：本書は「分析に使える可能性のある公開Data Sourceの候補一覧」である。Datasetが公開されていることは、当チームの提供Scope、商用利用可否、特定の因果効果のIdentification可能性を意味しない。License・原典・利用規約は実利用時に再確認する。

---

# 2. 一覧表

|No|カテゴリ|主な用途 / 分析候補|データ名|URL|レコード規模|典型フィールド|ライセンス / 利用条件|備考|
|---:|---|---|---|---|---|---|---|---|
|1|EC取引・配送|RFM、再購入、配送遅延、Seller/Customer分析|Brazilian E-Commerce Public Dataset by Olist|https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce|約100,000 orders|seller_id, customer_id, order_id, price, freight_value, timestamps|Kaggle上の利用条件を要確認|2016–2018年のブラジルEC実取引|
|2|ID-POS・実店舗購買|再購入、購買間隔、Propensity、Customer Value、販促分析|completejourney / Complete Journey 2.0|https://github.com/bradleyboehmke/completejourney|取引明細1,469,307行、2,469世帯、約1年間|household_id, store_id, basket_id, product_id, sales_value, discount, timestamp|CC0|商品・世帯属性・Campaign・Coupon・Promotion関連Tableを持つ|
|3|EC・Supply Chain|配送遅延、Lead Time、顧客/物流分析|DataCo SMART SUPPLY CHAIN FOR BIG DATA ANALYSIS|https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis|約180,519 records|Customer Id, Order Id, Sales, Shipping Mode, Days for shipping, Late_delivery_risk|CC0: Public Domain（当該Kaggle版）|約63列|
|4|EC・Supply Chain|配送・購買行動、clickstream分析|DataCo SMART SUPPLY CHAIN（別公開版）|https://www.kaggle.com/datasets/alinoranianesfahani/dataco-smart-supply-chain-for-big-data-analysis|約180,000 records + clickstream|Customer Id, Order Id, Shipping Mode, tokenized access logs|Apache 2.0（当該Kaggle版）|structured data + tokenized_access_logs.csv|
|5|ID-POS・実店舗購買|購買、販促、Customer Behavior|dunnhumby The Complete Journey|https://www.dunnhumby.com/source-files/|2,500世帯、2年間|household, basket, product, transaction, customer attributes, marketing history|research / personal / non-commercial|completejourneyとはLicense上別扱い|
|6|EC配送|On-time / Late Delivery Prediction|E-Commerce Shipping Data|https://www.kaggle.com/datasets/prachi13/customer-analytics|10,999 observations / 12 variables|Warehouse_block, Mode_of_Shipment, rating, Prior_purchases, Reached.on.Time_Y.N|Other / description参照|配送に特化|
|7|日本・事業者統計|外部特徴量、地域/業種Benchmark|e-Stat Economic Census for Business Frame|https://www.e-stat.go.jp/en/stat-search/database?toukei=00200552|統計表ごとに異なる|Establishments, Persons Engaged, Industry, Prefecture, Municipality|日本政府標準利用規約等|個票ではなく外部統計|
|8|EC購買履歴|Reorder、Next Basket、購買周期、推薦|Instacart Market Basket Analysis|https://www.kaggle.com/c/instacart-market-basket-analysis/data|約3.35 million orders / 約206,000 users|order_id, user_id, order_number, order_dow, days_since_prior_order, product_id|公開元・Kaggle条件要確認|1 userあたり4〜100 orders|
|9|EC取引|再購入、Churn/Inactivity、Customer Value|Online Retail|https://archive.ics.uci.edu/dataset/352/online+retail|541,909 transactions|InvoiceNo, StockCode, Quantity, InvoiceDate, UnitPrice, CustomerID, Country|CC BY 4.0|英国online retail実取引|
|10|EC行動ログ|Purchase / Add-to-cart、Recommendation、Conversion|RetailRocket Recommender System Dataset|https://www.kaggle.com/retailrocket/ecommerce-dataset/home|2,756,101 events、1,407,580 visitors|timestamp, visitorid, event, itemid, transactionid|CC BY-NC-SA 4.0|view / addtocart / transaction|
|11|EC配送|配送遅延、配送品質|Shipment Data of Ecommerce|https://www.kaggle.com/datasets/aayushsanjar/ecommerce-shipping-data|10,999 observations / 12 variables|Warehouse_block, Mode_of_Shipment, Weight, Reached.on.Time_Y.N|Kaggleページ要確認|E-Commerce Shipping Data再公開系|
|12|EC購買履歴|再購入、Customer Value、購買頻度|UCI Online Retail II|https://archive.ics.uci.edu/dataset/502/online%2Bretail%2Bii|1,067,371行、約2年間|InvoiceNo, StockCode, Quantity, InvoiceDate, UnitPrice, CustomerID|CC BY 4.0|英国online retail実取引|
|13|国際物流統計|物流市場外部特徴量|UPU Postal Statistics|https://www.upu.int/en/Universal-Postal-Union/Activities/Research-Publications/Postal-Statistics|国×年×統計項目|Country, Year, Parcel volumes, Revenue, Infrastructure|UPU条件要確認|国・地域Level|
|14|日本・物流統計|宅配市場Benchmark|国土交通省 宅配便取扱個数|https://www.mlit.go.jp/statistics/details/jidosha_list.html|年次集計|年度, 宅配便取扱個数, 便名別取扱個数, シェア|国交省利用規約等|個票ではない|
|15|審査・承認|Approval / Credit Risk|Credit Card Approval - With Target|https://www.kaggle.com/datasets/laotse/credit-card-approval|Kaggle上で要確認|申込者属性、信用履歴由来Target等|Kaggle表示要確認|派生・加工版の可能性|
|16|審査・信用リスク|Credit Risk|Credit Card Approval Prediction|https://www.kaggle.com/datasets/rikdifos/credit-card-approval-prediction|2 files、行数要確認|ID, demographic, income, employment, STATUS|Kaggle表示要確認|Target設計が必要な場合あり|
|17|支払遅滞・Default|Default Prediction|Credit Card Default Dataset|https://www.kaggle.com/datasets/ifeanyichukwunwobodo/credit-card-default|要確認|属性、利用状況、支払履歴、default|要確認|UCI由来の可能性、原典確認|
|18|支払遅滞・Default|Default Risk|Credit Card Default Risk Analysis|https://www.kaggle.com/competitions/npci-credit-card-default-risk-analysis/data|Competition page要確認|demographics, credit, payments, bills|Competition rules要確認|Competition形式|
|19|支払遅滞・Default|翌月Default|Default of Credit Card Clients Dataset|https://www.kaggle.com/datasets/uciml/default-of-credit-card-clients-dataset|30,000件、23特徴量|LIMIT_BAL, PAY_0-6, BILL_AMT, PAY_AMT, default|UCI原典 CC BY 4.0|代表的信用Risk benchmark|
|20|消費者信用|Credit Risk、Model Stability|Home Credit - Credit Risk Model Stability|https://www.kaggle.com/c/home-credit-credit-risk-model-stability/data|複数Table|case_id, date_decision, target, applicant, historical credit|Competition rules要確認|大規模Consumer Credit|
|21|審査・承認|Approval Classification|UCI Credit Approval|https://www.kaggle.com/datasets/echo9k/uci-credit-approval|690件、15特徴量|A1-A15, A16|UCI原典 CC BY 4.0|古典Benchmark|
|22|企業信用格付|Credit Rating|Corporate Credit Rating|https://www.kaggle.com/datasets/agewerc/corporate-credit-rating|2,029 records、31列|rating, date, sector, financial ratios|CC BY 4.0|2010–2016年中心|
|23|企業信用格付|Ordinal Credit Rating|Utilizing Historical Data for Corporate Credit Rating Assessment|https://data.mendeley.com/datasets/9fp8w335xf/1|901社、28特徴、22段階格付|quarterly financials, S&P rating|CC BY 4.0|Bloomberg/S&P由来情報|
|24|企業Default|Corporate Default|NewConnect market - corporate default prediction|https://www.kaggle.com/datasets/lukaszpostek/newconnect-market-corporate-default-prediction|4,211 obs、571社、168 defaults|26 financial indicators, default|CC BY-NC-SA 4.0|2007–2017|
|25|企業倒産|1–5年先Bankruptcy|Polish Companies Bankruptcy|https://archive.ics.uci.edu/dataset/365/polish%2Bcompanies%2Bbankruptcy%2Bdata|各5,910〜10,503 obs、65 features|64 financial ratios, bankruptcy label|CC BY 4.0|予測期間別5 Dataset|
|26|製造機械|Failure Prediction|AI4I 2020 Predictive Maintenance Dataset|https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset|10,000 × 14|temperature, speed, torque, wear, failure modes|CC BY 4.0|合成Data|
|27|購買・ERP Event Log|Lead Time、Next Activity、Delay、Process Mining|BPI Challenge 2019|https://research.tue.nl/en/datasets/bpi-challenge-2019/|251,734 cases、1,595,923 events|case ID, activity, timestamp, vendor, item, purchase document|4TU配布条件要確認|実業務Purchase-to-Pay Event Log|
|28|油圧設備|Condition / Failure State|Condition Monitoring of Hydraulic Systems|https://archive.ics.uci.edu/dataset/447/condition+monitoring+of+hydraulic+systems|2,205 cycles|pressure, flow, temp, vibration, cooler/valve/pump states|CC BY 4.0|実験設備多変量時系列|
|29|生産計画・SCM|MRP、Scheduling、Capacity Analysis|frePPLe Manufacturing Demo Dataset|https://frepple.com/docs/current/examples/manufacturing_demo.php|小規模Demo|item, location, demand, operation, resource, BOM, inventory|要個別確認|仮想製造企業、実観測ではない|
|30|回転機械|RUL、Failure、Anomaly|IMS Bearings|https://catalog.data.gov/dataset/ims-bearings|3 run-to-failure試験|timestamp, acceleration vibration|U.S. Government Works|実run-to-failure|
|31|販売・需要計画|Sales Forecast、Price/Promotion分析|M5 Forecasting - Accuracy|https://www.kaggle.com/competitions/m5-forecasting-accuracy/data|30,490系列、1,941日|item/store/state sales, sell_price, event, SNAP|Competition Rules|需要予測は当チーム代表例から除外|
|32|ERP Sample DB|BOM、WorkOrder、Inventory、SQL/ETL|Microsoft AdventureWorks|https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure|複数業務Table|Product, BOM, WorkOrder, Inventory, Purchase/SalesOrder|MIT|架空企業、実観測ではない|
|33|産業機械・音響|Acoustic Anomaly / Condition|MIMII Dataset|https://zenodo.org/records/3384388|約100 GB、4機種×複数個体|WAV, machine type/id, normal/anomaly, SNR|CC BY-SA 4.0|Valve/Pump/Fan/Slide Rail|
|34|設備保全|RUL、Degradation|NASA C-MAPSS Turbofan Engine Degradation Simulation|https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data|4 subsets|unit, cycle, settings, sensors|NASA公開条件|Simulation|
|35|工作機械|Tool Wear、RUL|NASA Milling Wear Dataset|https://data.nasa.gov/dataset/milling-wear|167 runs、16 conditions|VB, time, DOC, feed, current, vibration, acoustic emission|U.S. Government Works|工具摩耗|
|36|製造ライン|Condition / Degradation|Production Plant Data for Condition Monitoring|https://www.kaggle.com/datasets/inIT-OWL/production-plant-data-for-condition-monitoring|8 run-to-failure、10 CSV|process values, condition features|CC BY-SA 3.0|実製造Line由来|
|37|半導体製造|Pass/Fail、Quality Risk、Anomaly|SECOM|https://archive.ics.uci.edu/dataset/179/secom|1,567 × 約591|process sensors, Pass/Fail, Timestamp|CC BY 4.0|高次元・欠損・不均衡|
|38|製造品質|Defect Classification|Steel Plates Faults|https://archive.ics.uci.edu/dataset/198/steel+plates+faults|1,941、27特徴、7 classes|position, pixels, perimeter, luminosity, thickness|CC BY 4.0|鋼板欠陥|
|39|交通量|Traffic Flow / Congestion|JARTIC 断面交通量情報|https://www.jartic.or.jp/service/opendata/|51 folders、月次CSV|time, sensor/source, location, traffic volume|JARTIC利用規約、CC BY 4.0互換|毎月更新|
|40|自動運転・軌跡|Trajectory / Action Prediction|LOKI Dataset|https://usa.honda-ri.com/loki|644 scenarios、28,000+ agents|RGB, LiDAR, odometry, boxes, tracks, intended_actions|非商用・申請制|一般的な無条件Open Dataではない|
|41|交通事故|Severity / Risk / Hotspot|警察庁 交通事故統計情報Open Data|https://www.npa.go.jp/publications/statistics/koutsuu/opendata/index_opendata.html|事故1件1 record、2019–2024|date/time, location, parties, road, weather, signal, accident type|PDL1.0|CSV + definition/codebook|
|42|道路交通|Traffic Volume / Travel Speed|全国道路・街路交通情勢調査 一般交通量調査|https://www.mlit.go.jp/road/census/r3/|全国47都道府県|road, section, traffic volume, vehicle type, travel speed|PDL1.0準拠|CSV/Excel/PDF|
|43|GPS走行Log|Travel Time、Trajectory、Driving Behavior|会津若松市 公用車・公共交通車両走行情報|https://data.data4citizen.jp/dataset/10060158|継続収集、総数明記なし|vehicle, datetime, lat/lon, GPS error, 3-axis acceleration|CC BY|実車Log|
|44|金融・営業|Product Subscription / Sales Propensity|Bank Marketing|https://archive.ics.uci.edu/dataset/222/bank+marketing|最大45,211件|age, job, contact, duration, campaign, previous, poutcome, y|CC BY 4.0|電話営業成約Data|
|45|保険Cross-sell|Response / Cross-sell|Binary Classification of Insurance Cross Selling|https://www.kaggle.com/competitions/playground-series-s4e7/data|約1.2 GB、25列|Age, Previously_Insured, Vehicle, Premium, Sales_Channel, Response|CC BY 4.0|合成Data|
|46|Call Center Text|Sentiment、Call Type、Escalation等|Call Center Transcripts Dataset|https://www.kaggle.com/datasets/oleksiymaliovanyy/call-center-transcripts-dataset|件数明記なし|call type, sentiment, order/product, transcript|MIT|主にCustomer Service|
|47|企業Email Text|Classification、Priority、Communication分析|Enron Email Dataset|https://www.cs.cmu.edu/~enron/|約50万 emails、約150名|From, To, Date, Subject, Body|原版条件要確認|実企業Email、成約Labelなし|
|48|保険Cross-sell|Cross-sell Response|Health Insurance Cross Sell Prediction|https://www.kaggle.com/datasets/anmolkumar/health-insurance-cross-sell-prediction|train約381,000|Age, Vehicle, Premium, Sales_Channel, Response|GPL 2|自由記述なし|
|49|保険成約|Insurance Purchase Propensity|Insurance Company Benchmark (COIL 2000)|https://archive.ics.uci.edu/dataset/125/insurance+company+benchmark+coil+2000|train 5,822 + test 4,000、86 attrs|demographics, housing, purchasing power, insurance holdings, CARAVAN|CC BY 4.0|実Business Problem由来|
|50|営業会話Text|Conversation Classification / Intent|Sales Conversations|https://huggingface.co/datasets/goendalf666/sales-conversations|3,412 conversations|Customer/Salesman utterances, industry|要確認|GPT-3.5生成のSynthetic Data|
|51|Energy / Building|Energy Consumption Prediction|Appliances Energy Prediction|https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction|19,735 instances、29 features|Appliances, lights, temperature/humidity, weather, date|CC BY 4.0|既調査8件から統合|
|52|Environment|Air Quality / Pollutant Prediction|Beijing Multi-Site Air Quality|https://archive.ics.uci.edu/dataset/501/beijingmultisiteairqualitydata|420,768 hourly observations|PM2.5, PM10, SO2, NO2, CO, O3, weather, station|CC BY 4.0|既調査8件から統合|
|53|Industrial / Environment|CO / NOx Emission Prediction|Gas Turbine CO and NOx Emission Data Set|https://archive.ics.uci.edu/dataset/551/gas+turbine+co+and+nox+emission+data+set|36,733 instances、11 features|ambient/sensor variables, CO, NOx|CC BY 4.0|既調査8件から統合|
|54|Building|Occupancy Classification / Estimation|Occupancy Detection|https://archive.ics.uci.edu/|約20k observations（複数files）|temperature, humidity, light, CO2, humidity ratio, occupancy|UCI条件参照|既調査8件から統合|
|55|Engineering|Physical Performance Regression|Airfoil Self-Noise|https://archive.ics.uci.edu/dataset/291/airfoil+self+noise|1,503 instances、5 inputs + target|frequency, angle, chord, velocity, displacement thickness, sound pressure|CC BY 4.0|既調査8件から統合|
|56|Prognostics|RUL / Health State / Failure Prognostics|NASA Prognostics Data Repository / Open Data|https://data.nasa.gov/dataset/prognostics|Dataset collection|dataset-dependent sensor / degradation variables|NASA公開条件|C-MAPSS等を含むPrognostics系の入口として利用|

---

# 3. Datasetを分析用途で見る際の分類

## 3.1. 業務データ基盤型

一つのDatasetから複数のPrediction / Causal Questionを構成できるもの。

- completejourney
- Olist
- DataCo Supply Chain
- BPI Challenge 2019
- M5
- AdventureWorks

例：completejourneyでは、購買・再購入・Customer Value・Coupon利用・Campaign Exposure等を組み合わせて複数の問いを設計できる。

## 3.2. 明示Target型

比較的明確なPrediction Targetを持つもの。

- AI4I Machine Failure
- SECOM Pass / Fail
- Steel Plates Faults
- Default of Credit Card Clients
- Bank Marketing
- COIL 2000
- E-Commerce Shipping

## 3.3. 時系列 / Prognostics型

- C-MAPSS
- IMS Bearings
- NASA Milling Wear
- Hydraulic Systems
- Production Plant Condition Monitoring
- JARTIC
- 会津若松車両Log
- Appliances Energy
- Beijing Air Quality

## 3.4. Text / Interaction型

- Call Center Transcripts
- Enron Email
- Sales Conversations

## 3.5. Public Statistics / External Feature型

- e-Stat Economic Census
- UPU Postal Statistics
- 国土交通省 宅配便取扱個数
- 道路交通センサス

---

# 4. サービス紹介資料への示唆

Open Dataを統合すると、適用範囲は少なくとも以下に広がる。

```text
Customer / Commercial
- 解約
- 再購入
- 購買 / 成約
- Customer Value

Risk
- Fraud
- Credit / Default
- Bankruptcy
- Accident

Industrial / Quality
- Failure
- RUL / Degradation
- Defect / Pass-Fail

Operations / Process
- Delivery Delay
- Lead Time / Completion Time
- Process Deviation

Continuous / Forecast
- Energy
- Emission
- Traffic / Travel Time

Sequence / Interaction
- Trajectory
- Next Activity
- Text / Conversation Classification
```

したがって、サービス紹介資料でPredictive Analyticsを設備故障のみで代表させるのは適切ではない。

また、因果推論についても、Campaign、Coupon、Price、Process Change、Product Intervention等のTreatment候補を含むDatasetは存在するが、**Treatment列が存在することと因果効果を識別できることは別である**。因果分析の適用可否は、Treatment Assignment、Temporal Ordering、Confounding、Overlap、Experiment / Natural Experiment Design等を別途確認する必要がある。

---

# 5. 出所と作成上の留保

- 添付資料 `__open_data_source_ZZ_whole.md` の一覧・記載内容を統合の基礎とした。
- 既調査8件のうち、添付一覧に存在しなかったDatasetを追加した。
- 添付内に「要確認」と記載されたLicense・件数・原典は、本書でも要確認として保持した。推測で補完していない。
- Kaggle再公開版と原典Datasetが併存する場合がある。商用PoC、成果物配布、Model公開等を行う場合は原典Licenseを再確認する。
- Synthetic / Simulation / Demo / Non-commercial Datasetは、Method検証や説明用としては有用でも、そのまま商用利用できるとは限らない。