---
name: reference-salesforce-katsudo
description: 「活動」「活動データ」という言葉はOBIC（売上/仕入等の基幹データ）ではなくSalesforceの活動レコード（Task/Event）を指す
metadata:
  type: reference
---

「活動」「活動データ」と言われたら、OBIC7（基幹システム）ではなく **Salesforce** の活動レコードを指す。

- Salesforceの活動＝ `Task`（電話・その他等のToDo）および `Event`（訪問記録。Subjectが「訪問:取引先名」形式で入る）
- 訪問記録は主に `Event` オブジェクトに入っている（`Task` は更新が止まっている場合がある。2026年7月時点でTaskの最新は2026-05-01止まり、Eventは当日分まで入っていた）
- ボンド商事とウッド建材はSalesforce組織（scan-bwd）を共用しているため、会社を絞り込む場合は取引先（Account）の `code__c` フィールドで判別する：`B`始まり＝ボンド商事、`W`始まり＝ウッド建材
- 接続・データ構造の詳細は共有リポジトリの `Salesforce_MCP接続引継ぎ資料 1.md` を参照

関連：[[obic-katsudo-distinction]]
