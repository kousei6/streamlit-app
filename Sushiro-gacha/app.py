import streamlit as st
import random

# Global menu data
# 最新の画像URLに更新
SUSHiro_MENU = {
    "本鮪中とろ": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_6153.png"},
    "とろかつお": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_2400.png"},
    "厳選まぐろ赤身 煮切り醤油漬け": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_303.png"},
    "藻塩炭焼のサバたたき": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_2730.png"},
    "北海道産さんま": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_2407.png"},
    "炙り赤えびバター醤油": {"price": 200, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_8058.png"},
    "きすの天ぷらにぎり": {"price": 200, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_414.png"},
    "炙りまるごと帆立バター醤油": {"price": 250, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_2597.png"},
    "活〆真鯛 煮切り醤油漬け": {"price": 260, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_305.png"},
    "ひらめ食べ比べ (生・漬け)": {"price": 260, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/250716_2297_v1.png"},
    "いか飯風すしとゲソにぎり": {"price": 260, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/250625_2280.png"},
    "スシロー海鮮巻き重ね(秋)": {"price": 260, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_805.png"},
    "炙り牛タンにぎり": {"price": 280, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_242.png"},
    "天然きんきの炙り": {"price": 360, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/250611_2290_2.png"},
    "炙り牡蠣バター醤油": {"price": 360, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_309.png"},
    "うなぎ食べ比べ (白焼きレモンのせ・蒲焼き)": {"price": 360, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_2729.png"},
    "天然鮪ねぎとろと塩こんぶ手巻": {"price": 360, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_814.png"},
    "本ずわい蟹と天然鮪ねぎとろ手巻": {"price": 360, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_815.png"},
    "生サーモンづくし4種盛り": {"price": 780, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_2684.png"},
    "あさり入り 貝だし塩ラーメン": {"price": 460, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_3766_2.png"},
    "和歌山 豚骨しょうゆラーメン": {"price": 460, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_3041.png"},
    "茄子の味噌汁": {"price": 250, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_969.png"},
    "きのこたっぷり あんかけ茶碗蒸し": {"price": 290, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_971.png"},
    "秋の山海の幸 天ぷら盛り(えび天)": {"price": 450, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/250910_828.png"},
    "たら白子の天ぷら": {"price": 390, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_866.png"},
    "りんごと紅茶のパフェ": {"price": 330, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_3767.png"},
    "あったかアップルスイートポテト": {"price": 240, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/250910_751.png"},
    "厳選まぐろ赤身": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/250910_201.png"},
    "サーモン": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/240701_349_2.png"},
    "焼とろサーモン": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241008_000346.png"},
    "〆さば": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/231004_646-2.png"},
    "〆さば(ごま・ネギ)": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_647.png"},
    "赤えび": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/250625_355.png"},
    "えび": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/230802_209-3.png"},
    "甘えび": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/230531_210-2.png"},
    "黒みる貝": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_620_1.png"},
    "たまご": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/230802_400-3.png"},
    "生ハム": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_407.png"},
    "黒門伊勢屋のわさびなす": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/250528_405.png"},
    "まぐろ+たまご": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_2154.png"},
    "えび+たまご": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_2140.png"},
    "えび+サーモン": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_2138.png"},
    "えび+いか": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_2139.png"},
    "サーモン+たまご": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_2197.png"},
    "サーモン+いか": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_2199.png"},
    "サーモン+焼とろサーモン": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_2198.png"},
    "えび+生えび": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_2316.png"},
    "オニオンサーモン": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/240701_224_2.png"},
    "おろし焼とろサーモン": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/230802_225-3.png"},
    "サーモン チーズマヨ炙り": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_317.png"},
    "サーモン バジルマヨチーズ炙り": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_322.png"},
    "えんがわ": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/240701_234_2.png"},
    "生えび": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_203.png"},
    "炙り赤えび塩レモン": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_338.png"},
    "えび チーズマヨ炙り": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_316.png"},
    "えび バジルマヨチーズ炙り": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_321.png"},
    "えびアボカド": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_418.png"},
    "えび天にぎり": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/221116_419_2.png"},
    "天然アイスランド貝": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241008_002552_2.png"},
    "コウイカ": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/240529_2279_2.png"},
    "煮あなご": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/230802_222-3.png"},
    "グリルチキン": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/230531_257-3.png"},
    "豚塩カルビ": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_3162.png"},
    "こだわりハンバーグにぎり": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_423.png"},
    "活〆はまち": {"price": 160, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_204.png"},
    "新・まぐろのサラダ寿司": {"price": 160, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/250910_300-2.png"},
    "新・サーモンのサラダ寿司": {"price": 160, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/250910_278.png"},
    "塩麹漬けまぐろ": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241127_285.png"},
    "びん長まぐろ": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/240529_2346.png"},
    "生サーモン": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_370_1.png"},
    "サーモンアボカド": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_211.png"},
    "サーモン バジルモッツァレラ": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_617.png"},
    "活〆真鯛": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/20250407_356.png"},
    "天然真あじ": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/240319_2202-3.png"},
    "大えび": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_446.png"},
    "塩麹漬け赤えび": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/250806_286_v2.png"},
    "たこ": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/230802_260-3.png"},
    "うなぎの蒲焼き": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_331_v1.png"},
    "数の子": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_401-3.png"},
    "生ハム バジルモッツァレラ": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_653.png"},
    "大つぶ貝": {"price": 200, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_348_1.png"},
    "国産ほたて貝柱": {"price": 260, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/221001_237.png"},
    "特ネタ大とろ": {"price": 360, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_290.png"},
    "特ネタ大とろ焦がし醤油": {"price": 360, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_270.png"},
    "ぷちローセット": {"price": 580, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/240828_2383.png"},
    "じぶんでつくローセット": {"price": 580, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/250312_602.png"},
    "ねぎまぐろ軍艦": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_511.png"},
    "まぐろ山かけ軍艦": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_512.png"},
    "まぐろユッケ軍艦 卵黄醤油がけ": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_530.png"},
    "まぐたく軍艦": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_554.png"},
    "サーモンたたき軍艦": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_545.png"},
    "甘えび軍艦": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_510.png"},
    "いかオクラめかぶ軍艦": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/250528_504.png"},
    "かにみそ軍艦": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_523.png"},
    "たらマヨ軍艦": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_528.png"},
    "数の子松前漬け軍艦": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_578.png"},
    "コーン軍艦": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_506.png"},
    "ツナサラダ軍艦": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_505.png"},
    "シーサラダ軍艦": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_507.png"},
    "かに風サラダ軍艦": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_503.png"},
    "たまごサラダ軍艦": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_3461.png"},
    "小粒納豆軍艦": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_672.png"},
    "小粒納豆巻(ネギ抜き)": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_2132.png"},
    "きゅうり巻": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/221116_843.png"},
    "いなり": {"price": 120, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_862.png"},
    "うずらフライ軍艦": {"price": 140, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_542_1.png"},
    "鉄火巻": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/221001_844.png"},
    "まぐたく巻": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/220601_554.png"},
    "本ずわい蟹軍艦": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/221130_548.png"},
    "コク旨まぐろ醤油ラーメン": {"price": 390, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_901.png"},
    "きつねうどん": {"price": 330, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_3118.png"},
    "えび天うどん": {"price": 330, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_919.png"},
    "かけうどん": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_909png.png"},
    "あおさと海苔の味噌汁": {"price": 220, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241008_000918_2.png"},
    "あさりの味噌汁": {"price": 220, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_936.png"},
    "新・サーモンのサラダパフェ": {"price": 250, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/250910_808.png"},
    "新・えびのサラダパフェ": {"price": 250, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/250910_807.png"},
    "茶碗蒸し": {"price": 240, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_933.png"},
    "モッツァレラチーズ天ぷら": {"price": 280, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/240724_3060.png"},
    "かぼちゃの天ぷら": {"price": 150, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_892.png"},
    "フライドポテト": {"price": 150, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_988.png"},
    "どんぶりポテト": {"price": 390, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_3211.png"},
    "赤いかの唐揚げ": {"price": 360, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/230913_3100.png"},
    "まるごと海老の柚子こしょう天ぷら": {"price": 390, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/241002_895.png"},
    "生ビール　ジョッキ": {"price": 590, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/170301_981.png"},
    "生ビール　グラス": {"price": 430, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/221209_982_3.png"},
    "生貯蔵酒": {"price": 480, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/1115_975.png"},
    "翠（SUI）": {"price": 400, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/221001_3570.png"},
    "レモンサワー": {"price": 400, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/20240209_2193.png"},
    "角ハイボール": {"price": 400, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/221001_987.png"},
    "オールフリー": {"price": 440, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/200406_990.png"},
    "ペプシコーラ": {"price": 200, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_959.png"},
    "ポップメロンソーダ": {"price": 200, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_955.png"},
    "さわやか白ぶどう": {"price": 200, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_962.png"},
    "さわやか白ぶどうソーダ": {"price": 200, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_963.png"},
    "ホワイトウォーター": {"price": 200, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_948.png"},
    "ホワイトソーダ": {"price": 200, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_949.png"},
    "ウーロン茶": {"price": 200, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_973.png"},
    "ポンジュース": {"price": 180, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/250528_957.png"},
    "アイスコーヒー": {"price": 170, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_717.png"},
    "ホットコーヒー": {"price": 170, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_728.png"},
    "アイスカフェラテ": {"price": 200, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_747.png"},
    "ホットカフェラテ": {"price": 200, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_722.png"},
    "アップルジュース": {"price": 130, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/240529_719.png"},
    "オレンジジュース": {"price": 130, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/240529_718.png"},
    "ストロベリーバニラパフェ": {"price": 300, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/240529_738.png"},
    "北海道ミルクレープメルバ": {"price": 270, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/240529_733.png"},
    "かぼちゃのブリュレアチーズケーキ": {"price": 270, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_752.png"},
    "ショコラケーキリッチ": {"price": 250, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/230531_639.png"},
    "北海道ミルクレープ": {"price": 230, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/230531_782.png"},
    "カタラーナアイスブリュレ": {"price": 250, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/230531_779.png"},
    "クラシックプリン": {"price": 230, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/230721_3199.png"},
    "わらび餅と大学芋のどっちも盛り": {"price": 230, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/200515_679.png"},
    "大学いも": {"price": 130, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/230628_706.png"},
    "京都峯嵐堂のわらびもち": {"price": 150, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/251001_734.png"},
    "フローズンマンゴー": {"price": 150, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/231004_756.png"},
    "懐かしのメロンシャーベット": {"price": 130, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/160906_783.png"},
    "北海道バニラアイス（カップ）": {"price": 130, "image": "https://cmsimage.akindo-sushiro.co.jp/menu/170301_712.png"},
}

def gacha_1000yen():
    result_items = []
    total_price = 0
    available_items = list(SUSHiro_MENU.keys())
    random.shuffle(available_items)

    while total_price < 1000 and available_items:
        item_name = available_items.pop(0)
        item_data = SUSHiro_MENU[item_name]
        price = item_data["price"]
        image = item_data["image"]

        if total_price + price <= 1000:
            result_items.append({"name": item_name, "price": price, "image": image})
            total_price += price
        else:
            affordable_items = [
                i for i in available_items if SUSHiro_MENU[i]["price"] <= 1000 - total_price
            ]
            if affordable_items:
                affordable_item_name = random.choice(affordable_items)
                affordable_item_data = SUSHiro_MENU[affordable_item_name]
                result_items.append(
                    {"name": affordable_item_name, "price": affordable_item_data["price"], "image": affordable_item_data["image"]}
                )
                total_price += affordable_item_data["price"]
                available_items.remove(affordable_item_name)
            else:
                break
    return result_items, total_price

def gacha_one_item():
    item_name = random.choice(list(SUSHiro_MENU.keys()))
    item_data = SUSHiro_MENU[item_name]
    price = item_data["price"]
    image = item_data["image"]
    return {"name": item_name, "price": price, "image": image}

st.title("🍣 スシローガチャ")
st.markdown("1000円以内で何が食べられるか、ランダムに決めてみませんか？")
st.markdown(
    """
- **1000円ガチャ**: 1000円の予算内で、ランダムにスシローのメニューを選びます。
- **一品ガチャ**: スシローの全メニューから、ランダムに一品だけ選びます。
"""
)
st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("🍣 1000円ガチャを引く", use_container_width=True):
        st.session_state["gacha_type"] = "1000yen"
        st.session_state["result"] = gacha_1000yen()

with col2:
    if st.button("🍣 一品ガチャを引く", use_container_width=True):
        st.session_state["gacha_type"] = "one_item"
        st.session_state["result"] = gacha_one_item()

if "result" in st.session_state:
    st.divider()
    gacha_type = st.session_state["gacha_type"]

    if gacha_type == "1000yen":
        items, total_price = st.session_state["result"]
        st.header("1000円ガチャの結果")
        if items:
            st.success("🎉 結果が出ました！")
            st.subheader("おすすめのメニュー")
            for item in items:
                st.write(f"- **{item['name']}** : **{item['price']}円**")
                try:
                    # widthパラメータを追加してサイズを調整
                    st.image(item["image"], caption=item["name"], width=150)
                except Exception as e:
                    st.error(f"画像の表示に失敗しました: {e}")
            st.info(f"合計金額: **{total_price}円**")
        else:
            st.warning("😭 申し訳ありません、1000円以内の組み合わせが見つかりませんでした。再度お試しください。")

    elif gacha_type == "one_item":
        item = st.session_state["result"]
        st.header("一品ガチャの結果")
        st.success("🎉 結果が出ました！")
        st.subheader("今日のおすすめの一品")
        st.write(f"- **{item['name']}** : **{item['price']}円**")
        try:
            # widthパラメータを追加してサイズを調整
            st.image(item["image"], caption=item["name"], width=250)
        except Exception as e:
            st.error(f"画像の表示に失敗しました: {e}")
    
    st.divider()
