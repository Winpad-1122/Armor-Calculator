import tkinter as tk
from tkinter import ttk, colorchooser, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw
import os
import numpy as np
import math
import random
import copy
import threading
import time
import itertools
import gc
import shutil
import json

LANGUAGES = {
    "zh_CN": {
        "title": "盔甲颜色计算器",
        "current_status": "当前状态",
        "version": "版本:",
        "level": "填充层数:",
        "current_blend": "当前混合色:",
        "target_color": "目标色:",
        "delta_e": "ΔE:",
        "no_dye": "未添加染料",
        "sequence": "染料序列",
        "clear": "清空序列",
        "sequence_self": "序列",
        "dye_times": "染料有效使用次数",
        "dye_options": "可选染料",
        "export": "导出图片",
        "idle": "空闲。",
        "calculating": "序列计算中...",
        "done": "计算完成。",
        "migrating": "序列迁移中...",
        "migration_done": "迁移完成。",
        "export_success": "图片已保存在 {}",
        "error_no_image": "错误：没有图片可导出",
        "error_process": "错误：图片处理失败",
        "error": "错误：{}",
        "calc_sequence": "计算染料序列",
        "based_on": "(基于目标色)",
        "max_warning": "染料序列已达到最大容量 {} 个！",
        "gen_failed": "序列生成失败",
        "invalid_value": "无效值",
        "invalid_input": "请输入有效的数值",
        "invalid_number": "请输入有效的数字",
        "invalid_range": "请确保1<=起始<=结束<=20",
        "confirm": "确定",
        "cancel": "取消",
        "generating": "生成中...",
        "tip": "提示",
        "language": "语言:",
        "white": "白色",
        "orange": "橙色",
        "magenta": "品红",
        "light_blue": "淡蓝",
        "yellow": "黄色",
        "lime": "黄绿",
        "pink": "粉红",
        "gray": "灰色",
        "light_gray": "淡灰",
        "cyan": "青色",
        "purple": "紫色",
        "blue": "蓝色",
        "brown": "棕色",
        "green": "绿色",
        "red": "红色",
        "black": "黑色",
        "batch_render": "批量渲染",
        "batch_render_title": "批量渲染设置",
        "sequence_length": "序列长度:",
        "from_length": "从",
        "to_length": "到",
        "select_version": "选择版本:",
        "select_level": "选择层数:",
        "start_render": "开始渲染",
        "rendering": "渲染中...",
        "render_complete": "渲染完成！共生成 {} 张图片",
        "render_progress": "渲染进度: {}/{}",
        "select_all": "全选",
        "deselect_all": "取消全选",
        "exclude_duplicates": "忽略长度2序列的顺序颠倒",
        "render_settings": "渲染设置",
        "duplicate_hint": "仅对序列长度为2时有效（忽略颜色顺序颠倒）",
        "duplicate_disabled_hint": "当前长度范围不包含2，此选项无效",
        "invalid": "无效的操作：没有改变既有颜色。",
        "armor_type": "盔甲种类:",
        "body_type": "体型:",
        "helmet": "头盔",
        "chestplate": "胸甲",
        "leggings": "护腿",
        "boots": "靴子",
        "horse_armor": "马铠",
        "wolf_armor": "狼铠",
        "adult": "成年",
        "baby": "幼年",
        "je": "JE",
        "be": "BE",
        "select_body_type": "选择体型:",
        "select_armor_type": "选择盔甲种类:",
        "new_batch": "新批次",
        "batch": "批次",
        "batch_empty": "(空)",
        "batch_prefix": "批次",
        "clear_batch": "清空批次",
        "delete_batch": "删除批次",
        "batch_full": "批次{}已满！请创建或切换其他批次",
        "batch_created": "已创建批次 {}，当前批次 {}",
        "invalid_add": "无效加入：{} 没有改变整体混合色",
        "switch_batch": "已切换到批次 {}",
        "batch_count": "批次数量:",
        "sequence_len": "序列长度:",
        "je_batch_render": "JE批量渲染",
        "je_batch_hint": "序列长度固定，批次数量决定分割方式",
        "batch_disabled_hint": "序列长度≤2时不支持分批次",
        "damage_level": "损坏程度:",
        "intact": "完好",
        "slightly_damaged": "轻微损坏",
        "moderately_damaged": "中度损坏",
        "very_damaged": "重度损坏",
        "select_damage_level": "选择损坏程度:",
        "be_mode_no_batch": "BE模式不支持分批次",
        "batch_full_hint": "当前批次已满（9个），请点击「新批次」或切换到其他批次",
        "switch_to": "切换到 {}",
        "no_valid_sequences": "没有有效的序列需要渲染",
        "cancelling": "正在取消...",
        "enumerating": "枚举中...",
        "found_sequences": "已发现 {} 个有效序列",
        "enumerating_progress": "枚举中... {}",
        "resume_enumerating": "从长度 {} 恢复枚举...",
        "render_start": "开始渲染...",
        "deduping": "去重中...",
        "render_error": "渲染失败: {}",
        "image_saved": "图片已保存: {}",
        "version_switched": "切换到 {}",
        "body_switched": "切换到 {}",
        "damage_switched": "切换到 {}",
        "armor_switched": "切换到 {}",
        "be_max_length": "BE模式序列最大长度为20",
        "invalid_range": "请确保1<=起始<=结束<=20"
    },
    "zh_TW": {
        "title": "盔甲顏色計算器",
        "current_status": "目前狀態",
        "version": "版本:",
        "level": "填充層數:",
        "current_blend": "目前混合色:",
        "target_color": "目標色:",
        "delta_e": "ΔE:",
        "no_dye": "未添加染料",
        "sequence": "染料序列",
        "clear": "清空序列",
        "dye_times": "染料有效使用次數",
        "dye_options": "可選染料",
        "export": "匯出圖片",
        "idle": "空閒。",
        "calculating": "序列計算中...",
        "done": "計算完成。",
        "migrating": "序列遷移中...",
        "migration_done": "遷移完成。",
        "export_success": "圖片已保存在 {}",
        "error_no_image": "錯誤：沒有圖片可匯出",
        "error_process": "錯誤：圖片處理失敗",
        "error": "錯誤：{}",
        "calc_sequence": "計算染料序列",
        "sequence_self": "序列",
        "based_on": "(基於目標色)",
        "max_warning": "染料序列已達到最大容量 {} 個！",
        "gen_failed": "序列生成失敗",
        "invalid_value": "無效值",
        "invalid_input": "請輸入有效的數值",
        "invalid_number": "請輸入有效的數字",
        "invalid_range": "請確保1<=起始<=結束<=20",
        "confirm": "確定",
        "cancel": "取消",
        "generating": "生成中...",
        "tip": "提示",
        "language": "語言:",
        "white": "白色",
        "orange": "橙色",
        "magenta": "品紅",
        "light_blue": "淡藍",
        "yellow": "黃色",
        "lime": "黃綠",
        "pink": "粉紅",
        "gray": "灰色",
        "light_gray": "淡灰",
        "cyan": "青色",
        "purple": "紫色",
        "blue": "藍色",
        "brown": "棕色",
        "green": "綠色",
        "red": "紅色",
        "black": "黑色",
        "batch_render": "批量渲染",
        "batch_render_title": "批量渲染設置",
        "sequence_length": "序列長度:",
        "from_length": "從",
        "to_length": "到",
        "select_version": "選擇版本:",
        "select_level": "選擇層數:",
        "start_render": "開始渲染",
        "rendering": "渲染中...",
        "render_complete": "渲染完成！共生成 {} 張圖片",
        "render_progress": "渲染進度: {}/{}",
        "select_all": "全選",
        "deselect_all": "取消全選",
        "exclude_duplicates": "忽略長度2序列的順序顛倒",
        "render_settings": "渲染設置",
        "duplicate_hint": "僅對序列長度為2時有效（忽略顏色順序顛倒）",
        "duplicate_disabled_hint": "目前長度範圍不包含2，此選項無效",
        "invalid": "無效的操作：沒有改變既有顏色。",
        "armor_type": "盔甲種類:",
        "body_type": "體型:",
        "helmet": "頭盔",
        "chestplate": "胸甲",
        "leggings": "護腿",
        "boots": "靴子",
        "horse_armor": "馬鎧",
        "wolf_armor": "狼鎧",
        "adult": "成年",
        "baby": "幼年",
        "je": "JE",
        "be": "BE",
        "select_body_type": "選擇體型:",
        "select_armor_type": "選擇盔甲種類:",
        "new_batch": "新批次",
        "batch": "批次",
        "batch_empty": "(空)",
        "batch_prefix": "批次",
        "clear_batch": "清空批次",
        "delete_batch": "刪除批次",
        "batch_full": "批次{}已滿！請創建或切換其他批次",
        "batch_created": "已創建批次 {}，當前批次 {}",
        "invalid_add": "無效加入：{} 沒有改變整體混合色",
        "switch_batch": "已切換到批次 {}",
        "batch_count": "批次數量:",
        "sequence_len": "序列長度:",
        "je_batch_render": "JE批量渲染",
        "je_batch_hint": "序列長度固定，批次數量決定分割方式",
        "batch_disabled_hint": "序列長度≤2時不支援分批次",
        "damage_level": "損壞程度:",
        "intact": "完好",
        "slightly_damaged": "輕微損壞",
        "moderately_damaged": "中度損壞",
        "very_damaged": "重度損壞",
        "select_damage_level": "選擇損壞程度:",
        "be_mode_no_batch": "BE模式不支持分批次",
        "batch_full_hint": "當前批次已滿（9個），請點擊「新批次」或切換到其他批次",
        "switch_to": "切換到 {}",
        "no_valid_sequences": "沒有有效的序列需要渲染",
        "cancelling": "正在取消...",
        "enumerating": "枚舉中...",
        "found_sequences": "已發現 {} 個有效序列",
        "enumerating_progress": "枚舉中... {}",
        "resume_enumerating": "從長度 {} 恢復枚舉...",
        "render_start": "開始渲染...",
        "deduping": "去重中...",
        "render_error": "渲染失敗: {}",
        "image_saved": "圖片已保存: {}",
        "version_switched": "切換到 {}",
        "body_switched": "切換到 {}",
        "damage_switched": "切換到 {}",
        "armor_switched": "切換到 {}",
        "be_max_length": "BE模式序列最大長度為20",
        "invalid_range": "請確保1<=起始<=結束<=20"
    },
    "ja_JP": {
        "title": "防具色計算機",
        "current_status": "現在の状態",
        "version": "バージョン:",
        "level": "充填層数:",
        "current_blend": "現在の混合色:",
        "target_color": "目標色:",
        "delta_e": "ΔE:",
        "no_dye": "染料未追加",
        "sequence": "染料シーケンス",
        "clear": "シーケンスをクリア",
        "dye_times": "染料有効使用回数",
        "dye_options": "染料選択",
        "export": "画像をエクスポート",
        "idle": "アイドル。",
        "calculating": "シーケンス計算中...",
        "done": "計算完了。",
        "migrating": "シーケンス移行中...",
        "migration_done": "移行完了。",
        "export_success": "画像を保存しました: {}",
        "error_no_image": "エラー：画像がありません",
        "error_process": "エラー：画像処理失敗",
        "error": "エラー：{}",
        "calc_sequence": "染料シーケンスを計算",
        "based_on": "(目標色に基づく)",
        "max_warning": "染料シーケンスは最大容量 {} 個に達しました！",
        "gen_failed": "シーケンス生成失敗",
        "sequence_self": "シーケンス",
        "invalid_value": "無効な値",
        "invalid_input": "有効な数値を入力してください",
        "invalid_number": "有効な数値を入力してください",
        "invalid_range": "1<=開始<=終了<=20 を確認してください",
        "confirm": "確定",
        "cancel": "キャンセル",
        "generating": "生成中...",
        "tip": "ヒント",
        "language": "言語:",
        "white": "白",
        "orange": "オレンジ",
        "magenta": "マゼンタ",
        "light_blue": "水色",
        "yellow": "黄色",
        "lime": "黄緑",
        "pink": "ピンク",
        "gray": "灰色",
        "light_gray": "薄灰色",
        "cyan": "シアン",
        "purple": "紫",
        "blue": "青",
        "brown": "茶",
        "green": "緑",
        "red": "赤",
        "black": "黒",
        "batch_render": "バッチレンダリング",
        "batch_render_title": "バッチレンダリング設定",
        "sequence_length": "シーケンス長:",
        "from_length": "から",
        "to_length": "まで",
        "select_version": "バージョン選択:",
        "select_level": "レベル選択:",
        "start_render": "レンダリング開始",
        "rendering": "レンダリング中...",
        "render_complete": "レンダリング完了！ {} 枚の画像を生成しました",
        "render_progress": "レンダリング進捗: {}/{}",
        "select_all": "すべて選択",
        "deselect_all": "すべて解除",
        "exclude_duplicates": "長さ2シーケンスの順序逆転を無視",
        "render_settings": "レンダリング設定",
        "duplicate_hint": "シーケンス長が2の場合のみ有効（色の順序逆転を無視）",
        "duplicate_disabled_hint": "現在の長さ範囲に2が含まれていません、このオプションは無効です",
        "invalid": "無効な操作：既存の色は変更されていません。",
        "armor_type": "防具の種類:",
        "body_type": "体型:",
        "helmet": "ヘルメット",
        "chestplate": "チェストプレート",
        "leggings": "レギンス",
        "boots": "ブーツ",
        "horse_armor": "馬鎧",
        "wolf_armor": "オオカミの鎧",
        "adult": "大人",
        "baby": "幼体",
        "je": "JE",
        "be": "BE",
        "select_body_type": "体型を選択:",
        "select_armor_type": "防具の種類を選択:",
        "new_batch": "新バッチ",
        "batch": "バッチ",
        "batch_empty": "(空)",
        "batch_prefix": "バッチ",
        "clear_batch": "バッチをクリア",
        "delete_batch": "バッチを削除",
        "batch_full": "バッチ{}が満杯です！新しいバッチを作成するか、他のバッチに切り替えてください",
        "batch_created": "バッチ {} を作成しました、現在のバッチ {}",
        "invalid_add": "無効な追加：{} は全体の混合色を変更しませんでした",
        "switch_batch": "バッチ {} に切り替えました",
        "batch_count": "バッチ数:",
        "sequence_len": "シーケンス長:",
        "je_batch_render": "JEバッチレンダリング",
        "je_batch_hint": "シーケンス長は固定、バッチ数で分割方法を決定",
        "batch_disabled_hint": "シーケンス長≤2の場合はバッチ分割不可",
        "damage_level": "損傷レベル:",
        "intact": "無傷",
        "slightly_damaged": "軽度損傷",
        "moderately_damaged": "中度損傷",
        "very_damaged": "重度損傷",
        "select_damage_level": "損傷レベルを選択:",
        "be_mode_no_batch": "BEモードはバッチ分割をサポートしていません",
        "batch_full_hint": "現在のバッチが満杯です（9個）、「新バッチ」をクリックするか他のバッチに切り替えてください",
        "switch_to": "{} に切り替え",
        "no_valid_sequences": "有効なシーケンスがありません",
        "cancelling": "キャンセル中...",
        "enumerating": "列挙中...",
        "found_sequences": "{} 個の有効なシーケンスを発見",
        "enumerating_progress": "列挙中... {}",
        "resume_enumerating": "長さ {} から列挙を再開...",
        "render_start": "レンダリング開始...",
        "deduping": "重複排除中...",
        "render_error": "レンダリング失敗: {}",
        "image_saved": "画像を保存: {}",
        "version_switched": "{} に切り替え",
        "body_switched": "{} に切り替え",
        "damage_switched": "{} に切り替え",
        "armor_switched": "{} に切り替え",
        "be_max_length": "BEモードのシーケンス最大長は20です",
        "invalid_range": "1<=開始<=終了<=20 を確認してください"
    },
    "en_US": {
        "title": "Armor Color Calculator",
        "current_status": "Current Status",
        "version": "Version:",
        "level": "Fill Level:",
        "current_blend": "Current Blend:",
        "target_color": "Target Color:",
        "delta_e": "ΔE:",
        "no_dye": "No dye added",
        "sequence": "Dye Sequence (max 20)",
        "clear": "Clear Sequence",
        "dye_times": "Dye Usage Count",
        "dye_options": "Dye Options",
        "export": "Export Image",
        "idle": "Idle.",
        "calculating": "Calculating sequence...",
        "done": "Calculation complete.",
        "migrating": "Migrating sequence...",
        "migration_done": "Migration complete.",
        "export_success": "Image saved at {}",
        "error_no_image": "Error: No image to export",
        "error_process": "Error: Image processing failed",
        "error": "Error: {}",
        "calc_sequence": "Calculate Dye Sequence",
        "based_on": "(based on target color)",
        "max_warning": "Dye sequence has reached maximum capacity of {}!",
        "gen_failed": "Sequence generation failed",
        "sequence_self": "Sequence",
        "invalid_value": "Invalid Value",
        "invalid_input": "Please enter a valid value",
        "invalid_number": "Please enter a valid number",
        "invalid_range": "Please ensure 1<=start<=end<=20",
        "confirm": "Confirm",
        "cancel": "Cancel",
        "generating": "Generating...",
        "tip": "Tip",
        "language": "Language:",
        "white": "White",
        "orange": "Orange",
        "magenta": "Magenta",
        "light_blue": "Light Blue",
        "yellow": "Yellow",
        "lime": "Lime",
        "pink": "Pink",
        "gray": "Gray",
        "light_gray": "Light Gray",
        "cyan": "Cyan",
        "purple": "Purple",
        "blue": "Blue",
        "brown": "Brown",
        "green": "Green",
        "red": "Red",
        "black": "Black",
        "batch_render": "Batch Render",
        "batch_render_title": "Batch Render Settings",
        "sequence_length": "Sequence Length:",
        "from_length": "From",
        "to_length": "To",
        "select_version": "Select Version:",
        "select_level": "Select Level:",
        "start_render": "Start Render",
        "rendering": "Rendering...",
        "render_complete": "Render complete! Generated {} images",
        "render_progress": "Render progress: {}/{}",
        "select_all": "Select All",
        "deselect_all": "Deselect All",
        "exclude_duplicates": "Ignore reversed order for length-2 sequences",
        "render_settings": "Render Settings",
        "duplicate_hint": "Only effective for sequences of length 2 (ignores color order reversal)",
        "duplicate_disabled_hint": "Current length range does not include 2, this option is disabled",
        "invalid": "Invalid operation: no existing colors were changed.",
        "armor_type": "Armor Type:",
        "body_type": "Body Type:",
        "helmet": "Helmet",
        "chestplate": "Chestplate",
        "leggings": "Leggings",
        "boots": "Boots",
        "horse_armor": "Horse Armor",
        "wolf_armor": "Wolf Armor",
        "adult": "Adult",
        "baby": "Baby",
        "je": "JE",
        "be": "BE",
        "select_body_type": "Select Body Type:",
        "select_armor_type": "Select Armor Type:",
        "new_batch": "New Batch",
        "batch": "Batch",
        "batch_empty": "(Empty)",
        "batch_prefix": "Batch",
        "clear_batch": "Clear Batch",
        "delete_batch": "Delete Batch",
        "batch_full": "Batch {} is full! Please create or switch to another batch",
        "batch_created": "Created batch {}, current batch {}",
        "invalid_add": "Invalid addition: {} did not change the overall blend color",
        "switch_batch": "Switched to Batch {}",
        "batch_count": "Batch Count:",
        "sequence_len": "Sequence Length:",
        "je_batch_render": "JE Batch Render",
        "je_batch_hint": "Fixed sequence length, batch count determines split pattern",
        "batch_disabled_hint": "Batch splitting not supported for sequence length ≤ 2",
        "damage_level": "Damage Level:",
        "intact": "Intact",
        "slightly_damaged": "Slightly Damaged",
        "moderately_damaged": "Moderately Damaged",
        "very_damaged": "Very Damaged",
        "select_damage_level": "Select Damage Level:",
        "be_mode_no_batch": "BE mode does not support batch splitting",
        "batch_full_hint": "Current batch is full (9 items), please click 'New Batch' or switch to another batch",
        "switch_to": "Switched to {}",
        "no_valid_sequences": "No valid sequences to render",
        "cancelling": "Cancelling...",
        "enumerating": "Enumerating...",
        "found_sequences": "Found {} valid sequences",
        "enumerating_progress": "Enumerating... {}",
        "resume_enumerating": "Resuming enumeration from length {}...",
        "render_start": "Starting render...",
        "deduping": "Deduping...",
        "render_error": "Render failed: {}",
        "image_saved": "Image saved: {}",
        "version_switched": "Switched to {}",
        "body_switched": "Switched to {}",
        "damage_switched": "Switched to {}",
        "armor_switched": "Switched to {}",
        "be_max_length": "BE mode sequence maximum length is 20",
        "invalid_range": "Please ensure 1<=start<=end<=20"
    }
}


class ImageBlendApp:
    def __init__(self, root):
        self.root = root
        self.root.title("盔甲颜色计算器")
        self.root.geometry("1450x1050")

        self.current_lang = "zh_CN"
        self.lang = LANGUAGES[self.current_lang]

        self.hex_color = tk.StringVar(value="#FFFFFF")

        self.game_version = "BE"
        self.body_type = "adult"
        self.armor_type = "helmet"
        self.is_horse_armor = False
        self.is_wolf_armor = False
        
        self.damage_level = "intact"

        self.image_size = self.get_image_size()
        self.current_image_index = 0

        self.batches = [[]]
        self.current_batch_index = 0
        self.current_blend_color = (255, 255, 255)
        self.max_batch_size = 20

        self.default_color = "#A06540"

        self.target_color = (255, 255, 255)
        self.target_hex = "#FFFFFF"
        self.use_target = False

        self.is_generating = False
        self.is_migrating = False
        self.is_batch_rendering = False
        self.batch_cancelled = False
        self.status_timer = None

        self.color_data = [
            ("#F0F0F0", "白色", "white"),
            ("#9D9D97", "淡灰", "light_gray"),
            ("#474F52", "灰色", "gray"),
            ("#1D1D21", "黑色", "black"),
            ("#835432", "棕色", "brown"),
            ("#B02E26", "红色", "red"),
            ("#F9801D", "橙色", "orange"),
            ("#FED83D", "黄色", "yellow"),
            ("#80C71F", "黄绿", "lime"),
            ("#5E7C16", "绿色", "green"),
            ("#169C9C", "青色", "cyan"),
            ("#3AB3DA", "淡蓝", "light_blue"),
            ("#3C44AA", "蓝色", "blue"),
            ("#8932B8", "紫色", "purple"),
            ("#C74EBD", "品红", "magenta"),
            ("#F38BAA", "粉红", "pink")
        ]

        self.color_names = {
            "#F0F0F0": "white",
            "#9D9D97": "light_gray",
            "#474F52": "gray",
            "#1D1D21": "black",
            "#835432": "brown",
            "#B02E26": "red",
            "#F9801D": "orange",
            "#FED83D": "yellow",
            "#80C71F": "lime",
            "#5E7C16": "green",
            "#169C9C": "cyan",
            "#3AB3DA": "light_blue",
            "#3C44AA": "blue",
            "#8932B8": "purple",
            "#C74EBD": "magenta",
            "#F38BAA": "pink"
        }

        self.color_order = [
            "White", "Light_Gray", "Gray", "Black",
            "Brown", "Red", "Orange", "Yellow",
            "Lime", "Green", "Cyan", "Light_Blue",
            "Blue", "Purple", "Magenta", "Pink"
        ]

        self.color_abbr = {
            "white": "Wh",
            "light_gray": "Lg",
            "gray": "Gy",
            "black": "Bk",
            "brown": "Br",
            "red": "Rd",
            "orange": "Og",
            "yellow": "Yl",
            "lime": "Lm",
            "green": "Ge",
            "cyan": "Ca",
            "light_blue": "Lb",
            "blue": "Bu",
            "purple": "Pr",
            "magenta": "Mg",
            "pink": "Pk"
        }

        self.abbr_to_full = {
            "Wh": "White",
            "Lg": "Light_Gray",
            "Gy": "Gray",
            "Bk": "Black",
            "Br": "Brown",
            "Rd": "Red",
            "Og": "Orange",
            "Yl": "Yellow",
            "Lm": "Lime",
            "Ge": "Green",
            "Ca": "Cyan",
            "Lb": "Light_Blue",
            "Bu": "Blue",
            "Pr": "Purple",
            "Mg": "Magenta",
            "Pk": "Pink"
        }

        self.color_times = {
            "white": 0,
            "light_gray": 0,
            "gray": 0,
            "black": 0,
            "brown": 0,
            "red": 0,
            "orange": 0,
            "yellow": 0,
            "lime": 0,
            "green": 0,
            "cyan": 0,
            "light_blue": 0,
            "blue": 0,
            "purple": 0,
            "magenta": 0,
            "pink": 0
        }

        self.color_sort_order = {
            "white": 0,
            "light_gray": 1,
            "gray": 2,
            "black": 3,
            "brown": 4,
            "red": 5,
            "orange": 6,
            "yellow": 7,
            "lime": 8,
            "green": 9,
            "cyan": 10,
            "light_blue": 11,
            "blue": 12,
            "purple": 13,
            "magenta": 14,
            "pink": 15
        }

        self.images = []
        self.background_image = None
        self.overlay_image = None
        self.dye_images = {}
        self.dye_buttons = []
        self.dye_icon_labels = []
        self.all_buttons = []
        self.new_batch_btn = None
        self.batch_render_btn = None
        self.auto_frame = None
        self.body_btns = []
        self.damage_btns = []
        self.damage_frame = None

        self.output_dir = "output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.load_armor_images()
        self.load_dye_images()

        self.create_widgets()

        self.root.after(100, self.update_display)

    def get_image_size(self):
        if self.armor_type == "horse_armor":
            if self.game_version == "JE":
                return (712, 691)
            else:
                return (770, 745)
        
        if self.armor_type == "wolf_armor":
            return (772, 748)
        
        if self.body_type == "adult":
            sizes = {
                "helmet": (400, 322),
                "chestplate": (439, 440),
                "leggings": (256, 440),
                "boots": (288, 300)
            }
        else:
            sizes = {
                "helmet": (392, 368),
                "chestplate": (342, 317),
                "leggings": (186, 201),
                "boots": (159, 115)
            }
        return sizes.get(self.armor_type, (439, 440))

    def get_armor_path(self):
        if self.armor_type == "horse_armor":
            version_folder = "JE" if self.game_version == "JE" else "BE"
            return os.path.join("textures", "armor", "horse_armor", version_folder)
        if self.armor_type == "wolf_armor":
            return os.path.join("textures", "armor", "wolf_armor")
        return os.path.join("textures", "armor", self.body_type, self.armor_type)

    def get_dye_path(self, english_name):
        return os.path.join("textures", "dye", f"{english_name}.png")

    def set_status(self, text, auto_reset=False):
        if self.status_timer:
            self.root.after_cancel(self.status_timer)
            self.status_timer = None
        self.status_var.set(text)
        if auto_reset:
            self.status_timer = self.root.after(2000, lambda: self.set_status(self.lang["idle"]))

    def set_buttons_enabled(self, enabled):
        state = 'normal' if enabled else 'disabled'
        for btn in self.all_buttons:
            try:
                btn.config(state=state)
            except:
                pass

    def load_armor_images(self):
        default_img = Image.new('RGBA', self.image_size, color=(128, 128, 128, 255))
        self.images = []
        self.overlay_image = None
        self.background_image = None

        armor_path = self.get_armor_path()

        if self.armor_type == "wolf_armor":
            damage_suffix = {
                "intact": "",
                "slightly_damaged": "_sd",
                "moderately_damaged": "_md",
                "very_damaged": "_vd"
            }.get(self.damage_level, "")
            
            d_path = os.path.join(armor_path, f"wolf_armor{damage_suffix}_d.png")
            u_path = os.path.join(armor_path, f"wolf_armor{damage_suffix}_u.png")

            try:
                if os.path.exists(d_path):
                    img = Image.open(d_path).convert('RGBA')
                    img = self.resize_image(img, self.image_size[0], self.image_size[1])
                    self.background_image = img
                else:
                    img = default_img.copy()
                    draw = ImageDraw.Draw(img)
                    draw.text((50, 130), f"请替换:\n{d_path}", fill=(255, 255, 255, 255))
                    self.background_image = img
            except Exception:
                self.background_image = default_img.copy()

            try:
                if os.path.exists(u_path):
                    overlay = Image.open(u_path).convert('RGBA')
                    overlay = self.resize_image(overlay, self.image_size[0], self.image_size[1])
                    self.images = [overlay]
                else:
                    transparent = Image.new('RGBA', self.image_size, (0, 0, 0, 0))
                    self.images = [transparent]
            except Exception:
                transparent = Image.new('RGBA', self.image_size, (0, 0, 0, 0))
                self.images = [transparent]

            self.overlay_image = None
            return

        elif self.armor_type == "horse_armor":
            d_path = os.path.join(armor_path, "horse_armor_d.png")
            u_path = os.path.join(armor_path, "horse_armor_u.png")

            try:
                if os.path.exists(d_path):
                    img = Image.open(d_path).convert('RGBA')
                    img = self.resize_image(img, self.image_size[0], self.image_size[1])
                else:
                    img = default_img.copy()
                    draw = ImageDraw.Draw(img)
                    draw.text((50, 130), f"请替换:\n{d_path}", fill=(255, 255, 255, 255))
                self.images.append(img)
            except Exception:
                img = default_img.copy()
                self.images.append(img)

            try:
                if os.path.exists(u_path):
                    overlay = Image.open(u_path).convert('RGBA')
                    overlay = self.resize_image(overlay, self.image_size[0], self.image_size[1])
                    self.overlay_image = overlay
            except Exception:
                pass

        elif self.armor_type == "helmet":
            d_path = os.path.join(armor_path, "helmet_d.png")
            u_path = os.path.join(armor_path, "helmet_u.png")

            try:
                if os.path.exists(d_path):
                    img = Image.open(d_path).convert('RGBA')
                    img = self.resize_image(img, self.image_size[0], self.image_size[1])
                else:
                    img = default_img.copy()
                    draw = ImageDraw.Draw(img)
                    draw.text((50, 130), f"请替换:\n{d_path}", fill=(255, 255, 255, 255))
                self.images.append(img)
            except Exception:
                img = default_img.copy()
                self.images.append(img)

            try:
                if os.path.exists(u_path):
                    overlay = Image.open(u_path).convert('RGBA')
                    overlay = self.resize_image(overlay, self.image_size[0], self.image_size[1])
                    self.overlay_image = overlay
            except Exception:
                pass

        elif self.armor_type == "leggings":
            d_path = os.path.join(armor_path, "leggings_d.png")
            u_path = os.path.join(armor_path, "leggings_u.png")

            try:
                if os.path.exists(d_path):
                    img = Image.open(d_path).convert('RGBA')
                    img = self.resize_image(img, self.image_size[0], self.image_size[1])
                else:
                    img = default_img.copy()
                    draw = ImageDraw.Draw(img)
                    draw.text((50, 130), f"请替换:\n{d_path}", fill=(255, 255, 255, 255))
                self.images.append(img)
            except Exception:
                img = default_img.copy()
                self.images.append(img)

            try:
                if os.path.exists(u_path):
                    overlay = Image.open(u_path).convert('RGBA')
                    overlay = self.resize_image(overlay, self.image_size[0], self.image_size[1])
                    self.overlay_image = overlay
            except Exception:
                pass

        elif self.armor_type == "chestplate":
            img_path = os.path.join(armor_path, "chestplate.png")
            try:
                if os.path.exists(img_path):
                    img = Image.open(img_path).convert('RGBA')
                    img = self.resize_image(img, self.image_size[0], self.image_size[1])
                else:
                    img = default_img.copy()
                    draw = ImageDraw.Draw(img)
                    draw.text((50, 130), f"请替换:\n{img_path}", fill=(255, 255, 255, 255))
                self.images.append(img)
            except Exception:
                img = default_img.copy()
                self.images.append(img)

        elif self.armor_type == "boots":
            img_path = os.path.join(armor_path, "boots.png")
            try:
                if os.path.exists(img_path):
                    img = Image.open(img_path).convert('RGBA')
                    img = self.resize_image(img, self.image_size[0], self.image_size[1])
                else:
                    img = default_img.copy()
                    draw = ImageDraw.Draw(img)
                    draw.text((50, 130), f"请替换:\n{img_path}", fill=(255, 255, 255, 255))
                self.images.append(img)
            except Exception:
                img = default_img.copy()
                self.images.append(img)

        if not self.images:
            self.images.append(default_img.copy())

    def reload_images(self):
        self.load_armor_images()
        self.update_display()

    def get_dye_filename(self, english_name):
        return f"{english_name}.png"

    def get_english_name(self, hex_val):
        for h, _, en in self.color_data:
            if h == hex_val:
                return en
        return None

    def get_color_abbr(self, english_name):
        return self.color_abbr.get(english_name, english_name[:2])

    def get_color_full_name(self, english_name):
        full_names = {
            "white": "White",
            "light_gray": "Light_Gray",
            "gray": "Gray",
            "black": "Black",
            "brown": "Brown",
            "red": "Red",
            "orange": "Orange",
            "yellow": "Yellow",
            "lime": "Lime",
            "green": "Green",
            "cyan": "Cyan",
            "light_blue": "Light_Blue",
            "blue": "Blue",
            "purple": "Purple",
            "magenta": "Magenta",
            "pink": "Pink"
        }
        return full_names.get(english_name, english_name)

    def get_display_color_name(self, english_name):
        color_name_map = {
            "white": self.lang["white"],
            "light_gray": self.lang["light_gray"],
            "gray": self.lang["gray"],
            "black": self.lang["black"],
            "brown": self.lang["brown"],
            "red": self.lang["red"],
            "orange": self.lang["orange"],
            "yellow": self.lang["yellow"],
            "lime": self.lang["lime"],
            "green": self.lang["green"],
            "cyan": self.lang["cyan"],
            "light_blue": self.lang["light_blue"],
            "blue": self.lang["blue"],
            "purple": self.lang["purple"],
            "magenta": self.lang["magenta"],
            "pink": self.lang["pink"]
        }
        return color_name_map.get(english_name, english_name)

    def get_color_name_by_hex(self, hex_val):
        english_name = self.color_names.get(hex_val.upper(), hex_val)
        return self.get_display_color_name(english_name)

    def load_dye_images(self):
        self.dye_images = {}

        for hex_val, chinese_name, english_name in self.color_data:
            path = self.get_dye_path(english_name)
            try:
                if os.path.exists(path):
                    img = Image.open(path).convert('RGBA')
                    img = img.resize((16, 16), Image.Resampling.LANCZOS)
                    self.dye_images[hex_val] = ImageTk.PhotoImage(img)
                else:
                    r, g, b = self.hex_to_rgb(hex_val)
                    img = Image.new('RGBA', (16, 16), (r, g, b, 255))
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([0, 0, 15, 15], outline=(100, 100, 100), width=1)
                    self.dye_images[hex_val] = ImageTk.PhotoImage(img)
            except Exception:
                r, g, b = self.hex_to_rgb(hex_val)
                img = Image.new('RGBA', (16, 16), (r, g, b, 255))
                draw = ImageDraw.Draw(img)
                draw.rectangle([0, 0, 15, 15], outline=(100, 100, 100), width=1)
                self.dye_images[hex_val] = ImageTk.PhotoImage(img)

    def resize_image(self, img, target_width, target_height):
        orig_width, orig_height = img.size
        ratio = min(target_width / orig_width, target_height / orig_height)
        new_width = int(orig_width * ratio)
        new_height = int(orig_height * ratio)

        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        canvas = Image.new('RGBA', (target_width, target_height), (0, 0, 0, 0))
        x = (target_width - new_width) // 2
        y = (target_height - new_height) // 2
        canvas.paste(resized, (x, y))
        return canvas

    def blend_colors_je(self, colors):
        if not colors:
            return self.hex_to_rgb(self.default_color)

        n = len(colors)
        sumR = 0.0
        sumG = 0.0
        sumB = 0.0
        sumMax = 0.0

        for color in colors:
            r, g, b = self.hex_to_rgb(color)
            sumR += r
            sumG += g
            sumB += b
            sumMax += max(r, g, b)

        avgR = sumR / n
        avgG = sumG / n
        avgB = sumB / n
        avgMax = sumMax / n
        maxAvg = max(avgR, avgG, avgB)

        if maxAvg == 0:
            return (0, 0, 0)

        gain = avgMax / maxAvg
        resultR = int(math.floor(avgR * gain))
        resultG = int(math.floor(avgG * gain))
        resultB = int(math.floor(avgB * gain))

        return (max(0, min(255, resultR)), max(0, min(255, resultG)), max(0, min(255, resultB)))

    def blend_colors_be(self, colors):
        if not colors:
            return self.hex_to_rgb(self.default_color)

        sumR = 0
        sumG = 0
        sumB = 0
        n = len(colors)

        for color in colors:
            r, g, b = self.hex_to_rgb(color)
            sumR += r
            sumG += g
            sumB += b

        resultR = int(math.floor(sumR / n))
        resultG = int(math.floor(sumG / n))
        resultB = int(math.floor(sumB / n))

        return (max(0, min(255, resultR)), max(0, min(255, resultG)), max(0, min(255, resultB)))

    def blend_colors(self, colors):
        if self.game_version == "JE":
            return self.blend_colors_je(colors)
        else:
            return self.blend_colors_be(colors)

    def get_all_colors(self):
        result = []
        for batch in self.batches:
            result.extend(batch)
        return result

    def calculate_blend_color(self):
        all_colors = self.get_all_colors()
        if not all_colors:
            if self.armor_type == "wolf_armor":
                return (255, 255, 255)
            return self.hex_to_rgb(self.default_color)

        if self.game_version == "JE":
            result_color = None
            for batch in self.batches:
                if not batch:
                    continue
                if result_color is None:
                    result_color = self.blend_colors(batch)
                else:
                    colors_to_blend = [self.rgb_to_hex(result_color[0], result_color[1], result_color[2])] + batch
                    result_color = self.blend_colors(colors_to_blend)

            if result_color is None:
                if self.armor_type == "wolf_armor":
                    return (255, 255, 255)
                return self.hex_to_rgb(self.default_color)
            return result_color
        else:
            return self.blend_colors(all_colors)

    def calculate_blend_color_for_sequence(self, seq):
        if not seq:
            if self.armor_type == "wolf_armor":
                return (255, 255, 255)
            return self.hex_to_rgb(self.default_color)
        return self.blend_colors(seq)

    def calculate_delta_e(self, color1, color2):
        r1, g1, b1 = color1
        r2, g2, b2 = color2

        def rgb_to_lab(r, g, b):
            r = r / 255.0
            g = g / 255.0
            b = b / 255.0

            r = r / 12.92 if r <= 0.04045 else ((r + 0.055) / 1.055) ** 2.4
            g = g / 12.92 if g <= 0.04045 else ((g + 0.055) / 1.055) ** 2.4
            b = b / 12.92 if b <= 0.04045 else ((b + 0.055) / 1.055) ** 2.4

            x = r * 0.4124 + g * 0.3576 + b * 0.1805
            y = r * 0.2126 + g * 0.7152 + b * 0.0722
            z = r * 0.0193 + g * 0.1192 + b * 0.9505

            x_ref, y_ref, z_ref = 0.95047, 1.0, 1.08883

            x = x / x_ref if x / x_ref > 0.008856 else (x / x_ref * 903.3 + 16) / 116
            y = y / y_ref if y / y_ref > 0.008856 else (y / y_ref * 903.3 + 16) / 116
            z = z / z_ref if z / z_ref > 0.008856 else (z / z_ref * 903.3 + 16) / 116

            l = 116 * y - 16
            a = 500 * (x - y)
            b_lab = 200 * (y - z)

            return l, a, b_lab

        l1, a1, b1_lab = rgb_to_lab(r1, g1, b1)
        l2, a2, b2_lab = rgb_to_lab(r2, g2, b2)

        delta_l = l1 - l2
        delta_a = a1 - a2
        delta_b = b1_lab - b2_lab

        return math.sqrt(delta_l ** 2 + delta_a ** 2 + delta_b ** 2)

    def pick_target_color(self):
        color = colorchooser.askcolor(title=self.lang["target_color"], color=self.target_hex)
        if color and color[0] is not None:
            r, g, b = color[0]
            self.target_color = (int(r), int(g), int(b))
            self.target_hex = self.rgb_to_hex(int(r), int(g), int(b))
            self.use_target = True
            self.update_color_display()

    def crossover(self, parent1, parent2, available_colors):
        if not parent1 or not parent2:
            return [random.choice(available_colors)]

        length = max(len(parent1), len(parent2))
        child = []

        for i in range(length):
            if i < len(parent1) and i < len(parent2):
                child.append(parent1[i] if random.random() < 0.5 else parent2[i])
            elif i < len(parent1):
                child.append(parent1[i])
            else:
                child.append(parent2[i])

        return child

    def mutate(self, seq, available_colors, max_length):
        if not seq:
            return [random.choice(available_colors)]

        new_seq = seq.copy()

        for i in range(len(new_seq)):
            if random.random() < 0.1:
                new_seq[i] = random.choice(available_colors)

        if random.random() < 0.2 and len(new_seq) < max_length:
            new_seq.append(random.choice(available_colors))

        if random.random() < 0.2 and len(new_seq) > 1:
            del new_seq[random.randint(0, len(new_seq)-1)]

        return new_seq

    def auto_generate_sequence(self):
        if self.is_generating:
            return

        target_rgb = self.target_color
        available_colors = [h for h, _, _ in self.color_data]

        if self.game_version == "JE":
            max_length = None
        else:
            max_length = 20

        self.is_generating = True
        self.set_buttons_enabled(False)
        self.auto_gen_btn.config(text=self.lang["generating"], state='disabled')
        self.set_status(self.lang["calculating"])

        def evaluate_sequence_full(seq):
            if not seq:
                return float('inf')
            blend = self.calculate_blend_color_for_sequence(seq)
            color_delta = self.calculate_delta_e(blend, target_rgb)
            return color_delta

        def generate():
            def evaluate_sequence(seq):
                if not seq:
                    return float('inf')
                return evaluate_sequence_full(seq)

            population_size = 100
            generations = 3000
            elite_size = 5
            tournament_size = 3

            def create_individual():
                if self.game_version == "JE":
                    length = random.randint(1, 30)
                else:
                    length = random.randint(1, 20)
                return [random.choice(available_colors) for _ in range(length)]

            def crossover_improved(parent1, parent2):
                if len(parent1) < 2 or len(parent2) < 2:
                    return parent1.copy()

                pos1 = random.randint(1, len(parent1) - 1)
                pos2 = random.randint(1, len(parent2) - 1)

                child = parent1[:pos1] + parent2[pos2:]

                if self.game_version == "BE" and len(child) > 20:
                    child = child[:20]
                if not child:
                    child = [random.choice(available_colors)]

                return child

            def mutate_improved(seq):
                new_seq = seq.copy()

                for i in range(len(new_seq)):
                    if random.random() < 0.08:
                        new_seq[i] = random.choice(available_colors)

                if self.game_version == "JE":
                    if random.random() < 0.15:
                        new_seq.insert(random.randint(0, len(new_seq)), random.choice(available_colors))
                else:
                    if random.random() < 0.15 and len(new_seq) < 20:
                        new_seq.insert(random.randint(0, len(new_seq)), random.choice(available_colors))

                if random.random() < 0.15 and len(new_seq) > 1:
                    del new_seq[random.randint(0, len(new_seq)-1)]

                if self.game_version == "BE" and len(new_seq) > 20:
                    new_seq = new_seq[:20]

                return new_seq

            def local_search(seq):
                best_seq = seq.copy()
                best_score = evaluate_sequence(best_seq)

                for i in range(len(best_seq)):
                    original_color = best_seq[i]
                    for color in random.sample(available_colors, min(5, len(available_colors))):
                        if color == original_color:
                            continue
                        test_seq = best_seq.copy()
                        test_seq[i] = color
                        score = evaluate_sequence(test_seq)
                        if score < best_score:
                            best_score = score
                            best_seq = test_seq

                if self.game_version == "JE":
                    for color in random.sample(available_colors, min(3, len(available_colors))):
                        test_seq = best_seq + [color]
                        score = evaluate_sequence(test_seq)
                        if score < best_score:
                            best_score = score
                            best_seq = test_seq
                else:
                    if len(best_seq) < 20:
                        for color in random.sample(available_colors, min(3, len(available_colors))):
                            test_seq = best_seq + [color]
                            score = evaluate_sequence(test_seq)
                            if score < best_score:
                                best_score = score
                                best_seq = test_seq

                if len(best_seq) > 1:
                    for i in range(len(best_seq)):
                        test_seq = best_seq[:i] + best_seq[i+1:]
                        score = evaluate_sequence(test_seq)
                        if score < best_score:
                            best_score = score
                            best_seq = test_seq

                return best_seq

            population = [create_individual() for _ in range(population_size)]
            best_overall = None
            best_overall_score = float('inf')

            no_improvement_count = 0

            for generation in range(generations):
                scores = [evaluate_sequence(ind) for ind in population]

                sorted_pairs = sorted(zip(scores, population), key=lambda x: x[0])
                current_best_score = sorted_pairs[0][0]
                current_best = sorted_pairs[0][1]

                if current_best_score < best_overall_score:
                    best_overall_score = current_best_score
                    best_overall = current_best.copy()
                    no_improvement_count = 0
                else:
                    no_improvement_count += 1

                if generation % 100 == 0:
                    self.root.after(0, lambda: self.set_status(f"{self.lang['calculating']} ({generation}/{generations})"))

                if best_overall_score < 0.5:
                    break

                elite = [ind for _, ind in sorted_pairs[:elite_size]]

                new_population = elite.copy()

                while len(new_population) < population_size:
                    tournament_indices = random.sample(range(len(population)), tournament_size)
                    tournament_winners = sorted([(scores[i], population[i]) for i in tournament_indices], key=lambda x: x[0])
                    parent1 = tournament_winners[0][1]
                    parent2 = tournament_winners[1][1]

                    child = crossover_improved(parent1, parent2)
                    child = mutate_improved(child)
                    new_population.append(child)

                population = new_population

                if no_improvement_count > 200:
                    for i in range(population_size // 5):
                        idx = random.randint(0, population_size - 1)
                        population[idx] = create_individual()
                    no_improvement_count = 0

            final_scores = [evaluate_sequence(ind) for ind in population]
            final_best_idx = min(range(len(final_scores)), key=lambda i: final_scores[i])
            final_best = population[final_best_idx]

            if final_scores[final_best_idx] < best_overall_score:
                best_overall = final_best
                best_overall_score = final_scores[final_best_idx]

            if best_overall_score > 1.0:
                refined_seq = local_search(best_overall)
                if evaluate_sequence(refined_seq) < best_overall_score:
                    best_overall = refined_seq

            self.root.after(0, lambda: self.apply_generated_sequence(best_overall))

        thread = threading.Thread(target=generate)
        thread.daemon = True
        thread.start()

    def apply_generated_sequence(self, seq):
        self.is_generating = False
        self.auto_gen_btn.config(text=self.lang["calc_sequence"], state='normal')

        if not seq:
            self.set_buttons_enabled(True)
            self.set_status(self.lang["done"], auto_reset=True)
            messagebox.showinfo(self.lang["tip"], self.lang["gen_failed"])
            return

        if self.game_version == "JE":
            self.batches = []
            for i in range(0, len(seq), 9):
                self.batches.append(seq[i:i+9])
        else:
            self.batches = [seq[:20]]

        self.current_batch_index = len(self.batches) - 1
        for key in self.color_times:
            self.color_times[key] = 0
        for color in seq:
            english_name = self.get_english_name(color)
            if english_name and english_name in self.color_times:
                self.color_times[english_name] += 1

        self.update_times_display()
        self.update_sequence_display()
        self.update_display()

        self.set_buttons_enabled(True)
        self.set_status(self.lang["done"], auto_reset=True)

    def get_color_code_for_sort(self, hex_val):
        english_name = self.get_english_name(hex_val)
        return self.color_sort_order.get(english_name, 999)

    def sort_two_color_sequence(self, seq):
        if len(seq) != 2:
            return seq
        code1 = self.get_color_code_for_sort(seq[0])
        code2 = self.get_color_code_for_sort(seq[1])
        if code1 <= code2:
            return seq
        else:
            return [seq[1], seq[0]]

    def get_valid_sequence(self):
        all_colors = self.get_all_colors()
        if not all_colors:
            return []

        valid_seq = []
        temp_color = self.hex_to_rgb(self.default_color)
        for color in all_colors:
            r, g, b = self.hex_to_rgb(color)
            new_color = ((temp_color[0] + r) // 2, (temp_color[1] + g) // 2, (temp_color[2] + b) // 2)
            if new_color != temp_color:
                valid_seq.append(color)
                temp_color = new_color

        return valid_seq

    def split_sequence_into_batches(self, seq, batch_count):
        n = len(seq)
        if batch_count == 1:
            return [seq]
        
        results = []
        
        if batch_count - 1 > n - 1:
            return []
        
        for split_points in itertools.combinations(range(1, n), batch_count - 1):
            batch = []
            start = 0
            for point in split_points:
                batch.append(seq[start:point])
                start = point
            batch.append(seq[start:])
            results.append(batch)
        
        return results

    def get_batch_signature(self, batches):
        sig_parts = []
        for batch in batches:
            sorted_batch = sorted(batch, key=lambda x: self.get_color_code_for_sort(x))
            sig_parts.append(tuple(sorted_batch))
        return tuple(sig_parts)

    def open_batch_render_dialog(self):
        if self.game_version == "BE":
            self.open_be_batch_render_dialog()
        else:
            self.open_je_batch_render_dialog()

    def open_be_batch_render_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self.lang["batch_render_title"])
        dialog.geometry("500x720")
        dialog.transient(self.root)
        dialog.grab_set()

        main_frame = ttk.Frame(dialog, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text=self.lang["render_settings"], font=("Arial", 12, "bold")).pack(pady=(0, 10))

        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=5)

        length_frame = ttk.LabelFrame(main_frame, text=self.lang["sequence_length"])
        length_frame.pack(fill=tk.X, pady=5)

        length_inner = ttk.Frame(length_frame)
        length_inner.pack(pady=10, padx=10)

        ttk.Label(length_inner, text=self.lang["from_length"]).pack(side=tk.LEFT, padx=5)
        from_var = tk.StringVar(value="1")
        from_entry = ttk.Entry(length_inner, textvariable=from_var, width=5)
        from_entry.pack(side=tk.LEFT, padx=5)

        ttk.Label(length_inner, text=self.lang["to_length"]).pack(side=tk.LEFT, padx=5)
        to_var = tk.StringVar(value="2")
        to_entry = ttk.Entry(length_inner, textvariable=to_var, width=5)
        to_entry.pack(side=tk.LEFT, padx=5)

        body_frame = ttk.LabelFrame(main_frame, text=self.lang["select_body_type"])
        body_frame.pack(fill=tk.X, pady=5)

        body_inner = ttk.Frame(body_frame)
        body_inner.pack(pady=10, padx=10)

        body_var = tk.StringVar(value=self.body_type)
        body_buttons = []
        for body in ["adult", "baby"]:
            display_name = self.lang["adult"] if body == "adult" else self.lang["baby"]
            rb = ttk.Radiobutton(body_inner, text=display_name, variable=body_var, value=body)
            rb.pack(side=tk.LEFT, padx=5)
            body_buttons.append((body, rb))

        armor_frame = ttk.LabelFrame(main_frame, text=self.lang["select_armor_type"])
        armor_frame.pack(fill=tk.X, pady=5)

        armor_inner = ttk.Frame(armor_frame)
        armor_inner.pack(pady=10, padx=10)

        armor_var = tk.StringVar(value=self.armor_type)
        for armor in ["helmet", "chestplate", "leggings", "boots", "horse_armor", "wolf_armor"]:
            display_name = {
                "helmet": self.lang["helmet"],
                "chestplate": self.lang["chestplate"],
                "leggings": self.lang["leggings"],
                "boots": self.lang["boots"],
                "horse_armor": self.lang["horse_armor"],
                "wolf_armor": self.lang["wolf_armor"]
            }.get(armor, armor)
            rb = ttk.Radiobutton(armor_inner, text=display_name, variable=armor_var, value=armor)
            rb.pack(side=tk.LEFT, padx=5)

        def update_body_state(*args):
            selected_armor = armor_var.get()
            if selected_armor == "horse_armor" or selected_armor == "wolf_armor":
                for body, rb in body_buttons:
                    rb.config(state='disabled')
                body_var.set("adult")
            else:
                for body, rb in body_buttons:
                    rb.config(state='normal')

        armor_var.trace('w', update_body_state)
        update_body_state()

        damage_frame = ttk.LabelFrame(main_frame, text=self.lang["select_damage_level"])
        damage_frame.pack(fill=tk.X, pady=5)

        damage_inner = ttk.Frame(damage_frame)
        damage_inner.pack(pady=10, padx=10)

        damage_var = tk.StringVar(value="intact")
        damage_levels = ["intact", "slightly_damaged", "moderately_damaged", "very_damaged"]
        damage_display = {
            "intact": self.lang["intact"],
            "slightly_damaged": self.lang["slightly_damaged"],
            "moderately_damaged": self.lang["moderately_damaged"],
            "very_damaged": self.lang["very_damaged"]
        }

        for level in damage_levels:
            rb = ttk.Radiobutton(damage_inner, text=damage_display[level], variable=damage_var, value=level)
            rb.pack(anchor=tk.W, padx=5, pady=2)

        def update_damage_visibility(*args):
            if armor_var.get() == "wolf_armor":
                damage_frame.pack(fill=tk.X, pady=5)
            else:
                damage_frame.pack_forget()

        armor_var.trace('w', update_damage_visibility)
        update_damage_visibility()

        options_frame = ttk.LabelFrame(main_frame, text=self.lang["render_settings"])
        options_frame.pack(fill=tk.X, pady=5)

        options_inner = ttk.Frame(options_frame)
        options_inner.pack(pady=10, padx=10)

        exclude_duplicates_var = tk.BooleanVar(value=True)
        cb_exclude = ttk.Checkbutton(options_inner, text=self.lang["exclude_duplicates"], variable=exclude_duplicates_var)
        cb_exclude.pack(anchor=tk.W)

        info_label = ttk.Label(options_inner,
                               text=self.lang["duplicate_hint"],
                               font=("Arial", 8), foreground="gray", wraplength=400)
        info_label.pack(anchor=tk.W, pady=(5, 0))

        def update_checkbox_state(*args):
            try:
                from_len = int(from_var.get())
                to_len = int(to_var.get())
                if from_len <= 2 <= to_len:
                    cb_exclude.config(state='normal')
                    info_label.config(text=self.lang["duplicate_hint"])
                else:
                    cb_exclude.config(state='disabled')
                    info_label.config(text=self.lang["duplicate_disabled_hint"])
            except ValueError:
                pass

        from_var.trace('w', update_checkbox_state)
        to_var.trace('w', update_checkbox_state)

        update_checkbox_state()

        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=10)

        progress_var = tk.StringVar(value=self.lang["idle"])
        progress_label = ttk.Label(progress_frame, textvariable=progress_var, font=("Arial", 9))
        progress_label.pack()

        progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        progress_bar.pack(fill=tk.X, pady=5)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        def start_batch_render():
            try:
                from_len = int(from_var.get())
                to_len = int(to_var.get())
                if from_len < 1 or to_len > 20 or from_len > to_len:
                    messagebox.showwarning(self.lang["invalid_value"], self.lang["invalid_range"])
                    return

                selected_body = body_var.get()
                selected_armor = armor_var.get()
                exclude_duplicates = exclude_duplicates_var.get()
                selected_damage_level = damage_var.get()

                dialog.destroy()

                if selected_armor == "wolf_armor":
                    self.batch_render_wolf(from_len, to_len, selected_body, selected_armor, selected_damage_level, exclude_duplicates)
                else:
                    self.batch_render_be(from_len, to_len, selected_body, selected_armor, exclude_duplicates)
            except ValueError:
                messagebox.showwarning(self.lang["invalid_value"], self.lang["invalid_number"])

        start_btn = ttk.Button(btn_frame, text=self.lang["start_render"], command=start_batch_render, width=15)
        start_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = ttk.Button(btn_frame, text=self.lang["cancel"], command=dialog.destroy, width=15)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def open_je_batch_render_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title(self.lang["je_batch_render"])
        dialog.geometry("500x750")
        dialog.transient(self.root)
        dialog.grab_set()

        main_frame = ttk.Frame(dialog, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text=self.lang["render_settings"], font=("Arial", 12, "bold")).pack(pady=(0, 10))

        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=5)

        length_frame = ttk.LabelFrame(main_frame, text=self.lang["sequence_len"])
        length_frame.pack(fill=tk.X, pady=5)

        length_inner = ttk.Frame(length_frame)
        length_inner.pack(pady=10, padx=10)

        ttk.Label(length_inner, text=self.lang["sequence_length"]).pack(side=tk.LEFT, padx=5)
        seq_len_var = tk.StringVar(value="3")
        seq_len_entry = ttk.Entry(length_inner, textvariable=seq_len_var, width=5)
        seq_len_entry.pack(side=tk.LEFT, padx=5)

        batch_count_frame = ttk.LabelFrame(main_frame, text=self.lang["batch_count"])
        batch_count_frame.pack(fill=tk.X, pady=5)

        batch_count_inner = ttk.Frame(batch_count_frame)
        batch_count_inner.pack(pady=10, padx=10)

        ttk.Label(batch_count_inner, text=self.lang["batch_count"]).pack(side=tk.LEFT, padx=5)
        batch_count_var = tk.StringVar(value="2")
        batch_count_entry = ttk.Entry(batch_count_inner, textvariable=batch_count_var, width=5)
        batch_count_entry.pack(side=tk.LEFT, padx=5)

        batch_hint_label = ttk.Label(batch_count_inner, text="", font=("Arial", 8), foreground="red")
        batch_hint_label.pack(side=tk.LEFT, padx=5)

        def validate_batch_count(*args):
            try:
                seq_len = int(seq_len_var.get())
                if seq_len <= 2:
                    batch_count_entry.config(state='disabled')
                    batch_count_var.set("1")
                    batch_hint_label.config(text=self.lang["batch_disabled_hint"])
                else:
                    batch_count_entry.config(state='normal')
                    batch_hint_label.config(text="")
            except ValueError:
                pass

        seq_len_var.trace('w', validate_batch_count)
        validate_batch_count()

        body_frame = ttk.LabelFrame(main_frame, text=self.lang["select_body_type"])
        body_frame.pack(fill=tk.X, pady=5)

        body_inner = ttk.Frame(body_frame)
        body_inner.pack(pady=10, padx=10)

        body_var = tk.StringVar(value=self.body_type)
        body_buttons = []
        for body in ["adult", "baby"]:
            display_name = self.lang["adult"] if body == "adult" else self.lang["baby"]
            rb = ttk.Radiobutton(body_inner, text=display_name, variable=body_var, value=body)
            rb.pack(side=tk.LEFT, padx=5)
            body_buttons.append((body, rb))

        armor_frame = ttk.LabelFrame(main_frame, text=self.lang["select_armor_type"])
        armor_frame.pack(fill=tk.X, pady=5)

        armor_inner = ttk.Frame(armor_frame)
        armor_inner.pack(pady=10, padx=10)

        armor_var = tk.StringVar(value=self.armor_type)
        for armor in ["helmet", "chestplate", "leggings", "boots", "horse_armor", "wolf_armor"]:
            display_name = {
                "helmet": self.lang["helmet"],
                "chestplate": self.lang["chestplate"],
                "leggings": self.lang["leggings"],
                "boots": self.lang["boots"],
                "horse_armor": self.lang["horse_armor"],
                "wolf_armor": self.lang["wolf_armor"]
            }.get(armor, armor)
            rb = ttk.Radiobutton(armor_inner, text=display_name, variable=armor_var, value=armor)
            rb.pack(side=tk.LEFT, padx=5)

        def update_body_state(*args):
            selected_armor = armor_var.get()
            if selected_armor == "horse_armor" or selected_armor == "wolf_armor":
                for body, rb in body_buttons:
                    rb.config(state='disabled')
                body_var.set("adult")
            else:
                for body, rb in body_buttons:
                    rb.config(state='normal')

        armor_var.trace('w', update_body_state)
        update_body_state()

        damage_frame = ttk.LabelFrame(main_frame, text=self.lang["select_damage_level"])
        damage_frame.pack(fill=tk.X, pady=5)

        damage_inner = ttk.Frame(damage_frame)
        damage_inner.pack(pady=10, padx=10)

        damage_var = tk.StringVar(value="intact")
        damage_levels = ["intact", "slightly_damaged", "moderately_damaged", "very_damaged"]
        damage_display = {
            "intact": self.lang["intact"],
            "slightly_damaged": self.lang["slightly_damaged"],
            "moderately_damaged": self.lang["moderately_damaged"],
            "very_damaged": self.lang["very_damaged"]
        }

        for level in damage_levels:
            rb = ttk.Radiobutton(damage_inner, text=damage_display[level], variable=damage_var, value=level)
            rb.pack(anchor=tk.W, padx=5, pady=2)

        def update_damage_visibility(*args):
            if armor_var.get() == "wolf_armor":
                damage_frame.pack(fill=tk.X, pady=5)
            else:
                damage_frame.pack_forget()

        armor_var.trace('w', update_damage_visibility)
        update_damage_visibility()

        info_label = ttk.Label(main_frame, text=self.lang["je_batch_hint"],
                               font=("Arial", 8), foreground="gray", wraplength=450)
        info_label.pack(pady=5)

        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=10)

        progress_var = tk.StringVar(value=self.lang["idle"])
        progress_label = ttk.Label(progress_frame, textvariable=progress_var, font=("Arial", 9))
        progress_label.pack()

        progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        progress_bar.pack(fill=tk.X, pady=5)

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)

        def validate_inputs():
            try:
                seq_len = int(seq_len_var.get())
                if seq_len < 1 or seq_len > 30:
                    messagebox.showwarning(self.lang["invalid_value"], "序列长度必须在1-30之间")
                    return False
                if seq_len <= 2:
                    batch_count = 1
                else:
                    batch_count = int(batch_count_var.get())
                    if batch_count < 1 or batch_count > seq_len:
                        messagebox.showwarning(self.lang["invalid_value"], f"批次数量必须在1到{seq_len}之间")
                        return False
                    min_batches = math.ceil(seq_len / 9)
                    if batch_count < min_batches:
                        messagebox.showwarning(self.lang["invalid_value"], f"批次数量不能小于{min_batches}（{seq_len}个颜色每批最多9个）")
                        return False
                return True
            except ValueError:
                messagebox.showwarning(self.lang["invalid_value"], self.lang["invalid_number"])
                return False

        def start_batch_render():
            if not validate_inputs():
                return

            seq_len = int(seq_len_var.get())
            if seq_len <= 2:
                batch_count = 1
            else:
                batch_count = int(batch_count_var.get())
            selected_body = body_var.get()
            selected_armor = armor_var.get()
            selected_damage_level = damage_var.get()

            dialog.destroy()

            if selected_armor == "wolf_armor":
                self.batch_render_wolf_je(seq_len, batch_count, selected_body, selected_armor, selected_damage_level)
            else:
                self.batch_render_je(seq_len, batch_count, selected_body, selected_armor)

        start_btn = ttk.Button(btn_frame, text=self.lang["start_render"], command=start_batch_render, width=15)
        start_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = ttk.Button(btn_frame, text=self.lang["cancel"], command=dialog.destroy, width=15)
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def batch_render_wolf(self, from_len, to_len, body_type, armor_type, damage_level, exclude_duplicates):
        if self.is_batch_rendering:
            return
        
        self.is_batch_rendering = False
        self.batch_cancelled = False
        self.damage_level = damage_level
        self.batch_render_be_with_damage(from_len, to_len, body_type, armor_type, damage_level, exclude_duplicates)

    def batch_render_wolf_je(self, seq_len, batch_count, body_type, armor_type, damage_level):
        if self.is_batch_rendering:
            return
        
        self.is_batch_rendering = False
        self.batch_cancelled = False
        self.damage_level = damage_level
        self.batch_render_je_with_damage(seq_len, batch_count, body_type, armor_type, damage_level)

    def batch_render_be_with_damage(self, from_len, to_len, body_type, armor_type, damage_level, exclude_duplicates):
        if self.is_batch_rendering:
            return

        self.is_batch_rendering = True
        self.batch_cancelled = False
        self.set_buttons_enabled(False)
        self.set_status(self.lang["rendering"])

        available_colors = [h for h, _, _ in self.color_data]

        body_str = "adult" if body_type == "adult" else "baby"
        armor_str = armor_type
        
        damage_str = damage_level

        if from_len == to_len:
            folder_name = f"BE_{body_str}_{armor_str}_{damage_str}_Len{from_len}"
        else:
            folder_name = f"BE_{body_str}_{armor_str}_{damage_str}_Len{from_len}-{to_len}"

        batch_output_dir = os.path.join(self.output_dir, folder_name)
        if not os.path.exists(batch_output_dir):
            os.makedirs(batch_output_dir)

        cache_dir = os.path.join(self.output_dir, ".cache", folder_name)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        progress_file = os.path.join(cache_dir, "progress.txt")
        enumerated_file = os.path.join(cache_dir, "enumerated.txt")
        enumerate_progress_file = os.path.join(cache_dir, "enumerate_progress.txt")
        render_progress_file = os.path.join(cache_dir, "render_progress.txt")
        deduped_file = os.path.join(cache_dir, "deduped.txt")

        progress_dialog = tk.Toplevel(self.root)
        progress_dialog.title(self.lang["rendering"])
        progress_dialog.geometry("400x180")
        progress_dialog.transient(self.root)
        progress_dialog.protocol("WM_DELETE_WINDOW", lambda: None)

        progress_frame = ttk.Frame(progress_dialog, padding=15)
        progress_frame.pack(fill=tk.BOTH, expand=True)

        progress_label = ttk.Label(progress_frame, text=self.lang["idle"], font=("Arial", 10))
        progress_label.pack(pady=5)

        progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=350)
        progress_bar.pack(pady=10)

        status_label = ttk.Label(progress_frame, text="", font=("Arial", 8), foreground="gray")
        status_label.pack(pady=5)

        def cancel_batch():
            self.batch_cancelled = True
            self.set_status(self.lang["cancelling"], auto_reset=True)

        cancel_btn = ttk.Button(progress_frame, text=self.lang["cancel"], command=cancel_batch, width=15)
        cancel_btn.pack(pady=5)

        def update_progress(current, total, seq_info=""):
            try:
                progress_label.config(text=self.lang["render_progress"].format(current, total))
                progress_bar.config(value=(current / total) * 100 if total > 0 else 0)
                status_label.config(text=seq_info)
                progress_dialog.update()
            except:
                pass

        def read_progress_state():
            if os.path.exists(progress_file):
                try:
                    with open(progress_file, 'r', encoding='utf-8') as f:
                        data = {}
                        for line in f:
                            if '=' in line:
                                key, val = line.strip().split('=', 1)
                                data[key] = val
                        state = data.get('state', '')
                        total = int(data.get('total', 0))
                        current_index = int(data.get('current_index', 0))
                        return state, total, current_index
                except:
                    pass
            return '', 0, 0

        def write_progress_state(state, total, current_index):
            try:
                with open(progress_file, 'w', encoding='utf-8') as f:
                    f.write(f"state={state}\n")
                    f.write(f"total={total}\n")
                    f.write(f"current_index={current_index}\n")
            except:
                pass

        def append_enumerated_sequence(seq):
            try:
                with open(enumerated_file, 'a', encoding='utf-8') as f:
                    f.write(','.join(seq) + '\n')
            except:
                pass

        def load_enumerated_sequences():
            if os.path.exists(enumerated_file):
                try:
                    sequences = []
                    with open(enumerated_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                parts = line.split(',')
                                seq = [p for p in parts if p]
                                sequences.append(seq)
                    return sequences
                except:
                    pass
            return []

        def save_deduped_sequences(sequences):
            try:
                with open(deduped_file, 'w', encoding='utf-8') as f:
                    for seq in sequences:
                        f.write(','.join(seq) + '\n')
            except:
                pass

        def load_deduped_sequences():
            if os.path.exists(deduped_file):
                try:
                    sequences = []
                    with open(deduped_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                parts = line.split(',')
                                seq = [p for p in parts if p]
                                sequences.append(seq)
                    return sequences
                except:
                    pass
            return []

        def load_enumerate_progress():
            if os.path.exists(enumerate_progress_file):
                try:
                    with open(enumerate_progress_file, 'r', encoding='utf-8') as f:
                        line = f.read().strip()
                        if line:
                            return line.split(',')
                except:
                    pass
            return None

        def save_enumerate_progress(seq):
            try:
                with open(enumerate_progress_file, 'w', encoding='utf-8') as f:
                    if seq:
                        f.write(','.join(seq))
                    else:
                        f.write('')
            except:
                pass

        def load_render_progress():
            if os.path.exists(render_progress_file):
                try:
                    sequences = []
                    with open(render_progress_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                parts = line.split(',')
                                seq = [p for p in parts if p]
                                sequences.append(seq)
                    return sequences
                except:
                    pass
            return []

        def save_render_progress(seq):
            try:
                with open(render_progress_file, 'a', encoding='utf-8') as f:
                    f.write(','.join(seq) + '\n')
            except:
                pass

        def clear_cache():
            try:
                for f in [progress_file, enumerated_file, enumerate_progress_file, render_progress_file, deduped_file]:
                    if os.path.exists(f):
                        os.remove(f)
                if os.path.exists(cache_dir) and not os.listdir(cache_dir):
                    os.rmdir(cache_dir)
            except:
                pass

        def generate_sequences_with_progress(available_colors, from_len, to_len, start_length, start_seq):
            started = False if start_seq is not None else True

            for length in range(from_len, to_len + 1):
                if length < start_length:
                    continue
                elif length == start_length and start_seq is not None:
                    found_start = False
                    for seq in itertools.product(available_colors, repeat=length):
                        if not found_start:
                            if list(seq) == start_seq:
                                found_start = True
                                yield list(seq), length
                        else:
                            yield list(seq), length
                else:
                    for seq in itertools.product(available_colors, repeat=length):
                        yield list(seq), length

        def render_worker():
            try:
                old_body_type = self.body_type
                old_armor_type = self.armor_type
                old_image_size = self.image_size
                old_damage_level = self.damage_level

                self.body_type = body_type
                self.armor_type = armor_type
                self.damage_level = damage_level
                self.image_size = self.get_image_size()
                self.load_armor_images()
                self.load_dye_images()

                state, total, current_index = read_progress_state()
                deduped_sequences = load_deduped_sequences()

                if deduped_sequences:
                    state = 'rendering'
                    all_sequences = deduped_sequences
                else:
                    all_sequences = load_enumerated_sequences()

                enumerate_progress = load_enumerate_progress()
                rendered_sequences = load_render_progress()

                old_batches = copy.deepcopy(self.batches)
                old_times = self.color_times.copy()

                if state == 'rendering' and all_sequences:
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']}"))

                    start_idx = 0
                    if rendered_sequences:
                        last_rendered = rendered_sequences[-1]
                        for idx, seq in enumerate(all_sequences):
                            if seq == last_rendered:
                                start_idx = idx
                                break
                        if start_idx > 0:
                            rendered_sequences = rendered_sequences[:-1]
                            with open(render_progress_file, 'w', encoding='utf-8') as f:
                                for seq in rendered_sequences:
                                    f.write(','.join(seq) + '\n')

                    total = len(all_sequences)
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({start_idx+1}/{total})"))

                    for idx in range(start_idx, total):
                        if self.batch_cancelled:
                            break

                        seq = all_sequences[idx]
                        seq_names = [self.get_english_name(c) for c in seq]
                        seq_display = ", ".join(seq_names[:3])
                        if len(seq_names) > 3:
                            seq_display += f"... (+{len(seq_names)-3})"

                        if idx % 5 == 0 or idx == total - 1:
                            self.root.after(0, lambda i=idx, t=total, s=seq_display: update_progress(i+1, t, s))
                            self.root.after(0, lambda i=idx, t=total: self.set_status(f"{self.lang['rendering']} ({i+1}/{t})"))
                            write_progress_state('rendering', total, idx)

                        try:
                            self.batches = [seq.copy()]
                            self.current_batch_index = 0
                            for key in self.color_times:
                                self.color_times[key] = 0
                            for color in seq:
                                english_name = self.get_english_name(color)
                                if english_name and english_name in self.color_times:
                                    self.color_times[english_name] += 1

                            self.update_sequence_display()
                            self.update_times_display()
                            self.update_display()

                            final_img = self.render_single_image()

                            filename = self.generate_be_filename(seq, armor_type, body_type, damage_level) + ".png"
                            file_path = os.path.join(batch_output_dir, filename)
                            final_img.save(file_path, 'PNG')

                            del final_img

                            save_render_progress(seq)

                        except Exception as e:
                            print(self.lang["render_error"].format(e))

                        if (idx + 1) % 5 == 0:
                            try:
                                progress_dialog.update()
                            except:
                                pass
                            gc.collect()
                            time.sleep(0.05)

                        time.sleep(0.01)

                    if not self.batch_cancelled:
                        clear_cache()
                        self.root.after(0, lambda: self.set_status(self.lang["render_complete"].format(total), auto_reset=True))
                        self.root.after(0, lambda: messagebox.showinfo(self.lang["tip"], self.lang["render_complete"].format(total)))

                    self.body_type = old_body_type
                    self.armor_type = old_armor_type
                    self.damage_level = old_damage_level
                    self.image_size = old_image_size
                    self.batches = old_batches
                    self.color_times = old_times

                    self.load_armor_images()
                    self.load_dye_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()

                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['enumerating']})"))

                start_length = from_len
                start_seq = None

                if enumerate_progress:
                    start_seq = enumerate_progress
                    start_length = len(start_seq)
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['resume_enumerating'].format(start_length)})"))

                enumerate_count = 0
                if all_sequences:
                    enumerate_count = len(all_sequences)
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['found_sequences'].format(enumerate_count)})"))

                seq_generator = generate_sequences_with_progress(
                    available_colors, from_len, to_len, start_length, start_seq
                )

                for seq, length in seq_generator:
                    if self.batch_cancelled:
                        break

                    enumerate_count += 1

                    if enumerate_count % 10 == 0:
                        save_enumerate_progress(seq)
                        if enumerate_count % 100 == 0:
                            self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['enumerating_progress'].format(enumerate_count)})"))

                    self.batches = [[]]
                    self.current_batch_index = 0
                    for key in self.color_times:
                        self.color_times[key] = 0

                    all_valid = True
                    for color in seq:
                        if not self.add_color_to_sequence(color):
                            all_valid = False
                            break

                    if all_valid and len(self.get_all_colors()) == len(seq):
                        final_seq = self.get_all_colors().copy()
                        if len(final_seq) == 2:
                            final_seq = self.sort_two_color_sequence(final_seq)
                        append_enumerated_sequence(final_seq)

                if self.batch_cancelled:
                    self.body_type = old_body_type
                    self.armor_type = old_armor_type
                    self.damage_level = old_damage_level
                    self.image_size = old_image_size
                    self.batches = old_batches
                    self.color_times = old_times

                    self.load_armor_images()
                    self.load_dye_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()

                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                all_enumerated = load_enumerated_sequences()

                if not all_enumerated:
                    self.root.after(0, lambda: self.set_status(self.lang["error"].format(self.lang["no_valid_sequences"]), auto_reset=True))
                    messagebox.showinfo(self.lang["tip"], self.lang["no_valid_sequences"])

                    self.body_type = old_body_type
                    self.armor_type = old_armor_type
                    self.damage_level = old_damage_level
                    self.image_size = old_image_size
                    self.batches = old_batches
                    self.color_times = old_times

                    self.load_armor_images()
                    self.load_dye_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()

                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                if exclude_duplicates:
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['deduping']})"))
                    filtered_sequences = []
                    seen_signatures = set()

                    for seq in all_enumerated:
                        if len(seq) == 2:
                            sig = tuple(sorted(seq))
                        else:
                            sig = tuple(seq)

                        if sig not in seen_signatures:
                            seen_signatures.add(sig)
                            filtered_sequences.append(seq)

                    all_sequences = filtered_sequences
                else:
                    all_sequences = all_enumerated

                save_deduped_sequences(all_sequences)
                write_progress_state('rendering', len(all_sequences), 0)

                if not all_sequences:
                    self.root.after(0, lambda: self.set_status(self.lang["error"].format(self.lang["no_valid_sequences"]), auto_reset=True))
                    messagebox.showinfo(self.lang["tip"], self.lang["no_valid_sequences"])

                    self.body_type = old_body_type
                    self.armor_type = old_armor_type
                    self.damage_level = old_damage_level
                    self.image_size = old_image_size
                    self.batches = old_batches
                    self.color_times = old_times

                    self.load_armor_images()
                    self.load_dye_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()

                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['render_start']})"))

                total = len(all_sequences)
                for idx, seq in enumerate(all_sequences):
                    if self.batch_cancelled:
                        break

                    seq_names = [self.get_english_name(c) for c in seq]
                    seq_display = ", ".join(seq_names[:3])
                    if len(seq_names) > 3:
                        seq_display += f"... (+{len(seq_names)-3})"

                    if idx % 5 == 0 or idx == total - 1:
                        self.root.after(0, lambda i=idx, t=total, s=seq_display: update_progress(i+1, t, s))
                        self.root.after(0, lambda i=idx, t=total: self.set_status(f"{self.lang['rendering']} ({i+1}/{t})"))
                        write_progress_state('rendering', total, idx)

                    try:
                        self.batches = [seq.copy()]
                        self.current_batch_index = 0
                        for key in self.color_times:
                            self.color_times[key] = 0
                        for color in seq:
                            english_name = self.get_english_name(color)
                            if english_name and english_name in self.color_times:
                                self.color_times[english_name] += 1

                        self.update_sequence_display()
                        self.update_times_display()
                        self.update_display()

                        final_img = self.render_single_image()

                        filename = self.generate_be_filename(seq, armor_type, body_type, damage_level) + ".png"
                        file_path = os.path.join(batch_output_dir, filename)
                        final_img.save(file_path, 'PNG')

                        del final_img

                        save_render_progress(seq)

                    except Exception as e:
                        print(self.lang["render_error"].format(e))

                    if (idx + 1) % 5 == 0:
                        try:
                            progress_dialog.update()
                        except:
                            pass
                        gc.collect()
                        time.sleep(0.05)

                    time.sleep(0.01)

                if not self.batch_cancelled:
                    clear_cache()
                    self.root.after(0, lambda: self.set_status(self.lang["render_complete"].format(total), auto_reset=True))
                    self.root.after(0, lambda: messagebox.showinfo(self.lang["tip"], self.lang["render_complete"].format(total)))

                self.body_type = old_body_type
                self.armor_type = old_armor_type
                self.damage_level = old_damage_level
                self.image_size = old_image_size
                self.batches = old_batches
                self.color_times = old_times

                self.load_armor_images()
                self.load_dye_images()
                self.update_sequence_display()
                self.update_times_display()
                self.update_display()

                try:
                    progress_dialog.destroy()
                except:
                    pass
                self.is_batch_rendering = False
                self.set_buttons_enabled(True)

            except Exception as e:
                try:
                    progress_dialog.destroy()
                except:
                    pass
                self.is_batch_rendering = False
                self.set_buttons_enabled(True)
                self.root.after(0, lambda: self.set_status(self.lang["error"].format(str(e)), auto_reset=True))
                messagebox.showerror(self.lang["error"], str(e))

        thread = threading.Thread(target=render_worker)
        thread.daemon = True
        thread.start()

    def batch_render_je_with_damage(self, seq_len, batch_count, body_type, armor_type, damage_level):
        if self.is_batch_rendering:
            return

        if seq_len <= 2:
            batch_count = 1

        self.is_batch_rendering = True
        self.batch_cancelled = False
        self.set_buttons_enabled(False)
        self.set_status(self.lang["rendering"])

        available_colors = [h for h, _, _ in self.color_data]

        body_str = "adult" if body_type == "adult" else "baby"
        armor_str = armor_type
        
        damage_str = damage_level

        if seq_len <= 2:
            folder_name = f"JE_{body_str}_{armor_str}_{damage_str}_Len{seq_len}"
        else:
            folder_name = f"JE_{body_str}_{armor_str}_{damage_str}_Len{seq_len}_Batches{batch_count}"

        batch_output_dir = os.path.join(self.output_dir, folder_name)
        if not os.path.exists(batch_output_dir):
            os.makedirs(batch_output_dir)

        cache_dir = os.path.join(self.output_dir, ".cache", folder_name)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        progress_file = os.path.join(cache_dir, "progress.txt")
        enumerated_file = os.path.join(cache_dir, "enumerated.txt")
        enumerate_progress_file = os.path.join(cache_dir, "enumerate_progress.txt")
        render_progress_file = os.path.join(cache_dir, "render_progress.txt")
        deduped_file = os.path.join(cache_dir, "deduped.txt")

        progress_dialog = tk.Toplevel(self.root)
        progress_dialog.title(self.lang["rendering"])
        progress_dialog.geometry("400x200")
        progress_dialog.transient(self.root)
        progress_dialog.protocol("WM_DELETE_WINDOW", lambda: None)

        progress_frame = ttk.Frame(progress_dialog, padding=15)
        progress_frame.pack(fill=tk.BOTH, expand=True)

        progress_label = ttk.Label(progress_frame, text=self.lang["idle"], font=("Arial", 10))
        progress_label.pack(pady=5)

        progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=350)
        progress_bar.pack(pady=10)

        status_label = ttk.Label(progress_frame, text="", font=("Arial", 8), foreground="gray")
        status_label.pack(pady=5)

        def cancel_batch():
            self.batch_cancelled = True
            status_label.config(text=self.lang["cancelling"])

        cancel_btn = ttk.Button(progress_frame, text=self.lang["cancel"], command=cancel_batch, width=15)
        cancel_btn.pack(pady=5)

        def update_progress(current, total, seq_info=""):
            try:
                progress_label.config(text=self.lang["render_progress"].format(current, total))
                progress_bar.config(value=(current / total) * 100 if total > 0 else 0)
                status_label.config(text=seq_info)
                progress_dialog.update()
            except:
                pass

        def read_progress_state():
            if os.path.exists(progress_file):
                try:
                    with open(progress_file, 'r', encoding='utf-8') as f:
                        data = {}
                        for line in f:
                            if '=' in line:
                                key, val = line.strip().split('=', 1)
                                data[key] = val
                        state = data.get('state', '')
                        total = int(data.get('total', 0))
                        current_index = int(data.get('current_index', 0))
                        return state, total, current_index
                except:
                    pass
            return '', 0, 0

        def write_progress_state(state, total, current_index):
            try:
                with open(progress_file, 'w', encoding='utf-8') as f:
                    f.write(f"state={state}\n")
                    f.write(f"total={total}\n")
                    f.write(f"current_index={current_index}\n")
            except:
                pass

        def append_enumerated_sequence(seq):
            try:
                with open(enumerated_file, 'a', encoding='utf-8') as f:
                    f.write(','.join(seq) + '\n')
            except:
                pass

        def load_enumerated_sequences():
            if os.path.exists(enumerated_file):
                try:
                    sequences = []
                    with open(enumerated_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                parts = line.split(',')
                                seq = [p for p in parts if p]
                                sequences.append(seq)
                    return sequences
                except:
                    pass
            return []

        def save_deduped_sequences(sequences):
            try:
                with open(deduped_file, 'w', encoding='utf-8') as f:
                    for seq in sequences:
                        f.write(','.join(seq) + '\n')
            except:
                pass

        def load_deduped_sequences():
            if os.path.exists(deduped_file):
                try:
                    sequences = []
                    with open(deduped_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                parts = line.split(',')
                                seq = [p for p in parts if p]
                                sequences.append(seq)
                    return sequences
                except:
                    pass
                return []

        def load_enumerate_progress():
            if os.path.exists(enumerate_progress_file):
                try:
                    with open(enumerate_progress_file, 'r', encoding='utf-8') as f:
                        line = f.read().strip()
                        if line:
                            return line.split(',')
                except:
                    pass
            return None

        def save_enumerate_progress(seq):
            try:
                with open(enumerate_progress_file, 'w', encoding='utf-8') as f:
                    if seq:
                        f.write(','.join(seq))
                    else:
                        f.write('')
            except:
                pass

        def load_render_progress():
            if os.path.exists(render_progress_file):
                try:
                    sequences = []
                    with open(render_progress_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                parts = line.split(',')
                                seq = [p for p in parts if p]
                                sequences.append(seq)
                    return sequences
                except:
                    pass
            return []

        def save_render_progress(seq):
            try:
                with open(render_progress_file, 'a', encoding='utf-8') as f:
                    f.write(','.join(seq) + '\n')
            except:
                pass

        def clear_cache():
            try:
                for f in [progress_file, enumerated_file, enumerate_progress_file, render_progress_file, deduped_file]:
                    if os.path.exists(f):
                        os.remove(f)
                if os.path.exists(cache_dir) and not os.listdir(cache_dir):
                    os.rmdir(cache_dir)
            except:
                pass

        def generate_sequences_with_progress(available_colors, from_len, to_len, start_length, start_seq):
            for length in range(from_len, to_len + 1):
                if length < start_length:
                    continue
                elif length == start_length and start_seq is not None:
                    found_start = False
                    for seq in itertools.product(available_colors, repeat=length):
                        if not found_start:
                            if list(seq) == start_seq:
                                found_start = True
                                yield list(seq), length
                        else:
                            yield list(seq), length
                else:
                    for seq in itertools.product(available_colors, repeat=length):
                        yield list(seq), length

        def render_worker():
            try:
                old_body_type = self.body_type
                old_armor_type = self.armor_type
                old_image_size = self.image_size
                old_damage_level = self.damage_level

                self.body_type = body_type
                self.armor_type = armor_type
                self.damage_level = damage_level
                self.image_size = self.get_image_size()
                self.load_armor_images()
                self.load_dye_images()

                state, total, current_index = read_progress_state()
                deduped_sequences = load_deduped_sequences()

                if deduped_sequences:
                    state = 'rendering'
                    all_sequences = deduped_sequences
                else:
                    all_sequences = load_enumerated_sequences()

                enumerate_progress = load_enumerate_progress()
                rendered_sequences = load_render_progress()

                old_batches = copy.deepcopy(self.batches)
                old_times = self.color_times.copy()

                if state == 'rendering' and all_sequences:
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']}"))

                    start_idx = 0
                    if rendered_sequences:
                        last_rendered = rendered_sequences[-1]
                        for idx, seq in enumerate(all_sequences):
                            if seq == last_rendered:
                                start_idx = idx
                                break
                        if start_idx > 0:
                            rendered_sequences = rendered_sequences[:-1]
                            with open(render_progress_file, 'w', encoding='utf-8') as f:
                                for seq in rendered_sequences:
                                    f.write(','.join(seq) + '\n')

                    total = len(all_sequences)
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({start_idx+1}/{total})"))

                    for idx in range(start_idx, total):
                        if self.batch_cancelled:
                            break

                        seq = all_sequences[idx]
                        seq_names = [self.get_english_name(c) for c in seq]
                        seq_display = ", ".join(seq_names[:3])
                        if len(seq_names) > 3:
                            seq_display += f"... (+{len(seq_names)-3})"

                        if idx % 5 == 0 or idx == total - 1:
                            self.root.after(0, lambda i=idx, t=total, s=seq_display: update_progress(i+1, t, s))
                            self.root.after(0, lambda i=idx, t=total: self.set_status(f"{self.lang['rendering']} ({i+1}/{t})"))
                            write_progress_state('rendering', total, idx)

                        try:
                            self.batches = [seq.copy()]
                            self.current_batch_index = 0
                            for key in self.color_times:
                                self.color_times[key] = 0
                            for color in seq:
                                english_name = self.get_english_name(color)
                                if english_name and english_name in self.color_times:
                                    self.color_times[english_name] += 1

                            self.update_sequence_display()
                            self.update_times_display()
                            self.update_display()

                            final_img = self.render_single_image()

                            filename = self.generate_je_filename(seq, armor_type, body_type, damage_level) + ".png"
                            file_path = os.path.join(batch_output_dir, filename)
                            final_img.save(file_path, 'PNG')

                            del final_img

                            save_render_progress(seq)

                        except Exception as e:
                            print(self.lang["render_error"].format(e))

                        if (idx + 1) % 5 == 0:
                            try:
                                progress_dialog.update()
                            except:
                                pass
                            gc.collect()
                            time.sleep(0.05)

                        time.sleep(0.01)

                    if not self.batch_cancelled:
                        clear_cache()
                        self.root.after(0, lambda: self.set_status(self.lang["render_complete"].format(total), auto_reset=True))
                        self.root.after(0, lambda: messagebox.showinfo(self.lang["tip"], self.lang["render_complete"].format(total)))

                    self.body_type = old_body_type
                    self.armor_type = old_armor_type
                    self.damage_level = old_damage_level
                    self.image_size = old_image_size
                    self.batches = old_batches
                    self.color_times = old_times

                    self.load_armor_images()
                    self.load_dye_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()

                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['enumerating']})"))

                start_length = seq_len if seq_len <= 2 else 1
                start_seq = None

                if enumerate_progress:
                    start_seq = enumerate_progress
                    start_length = len(start_seq)
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['resume_enumerating'].format(start_length)})"))

                enumerate_count = 0
                if all_sequences:
                    enumerate_count = len(all_sequences)
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['found_sequences'].format(enumerate_count)})"))

                seq_generator = generate_sequences_with_progress(
                    available_colors, seq_len, seq_len, start_length, start_seq
                )

                for seq, length in seq_generator:
                    if self.batch_cancelled:
                        break

                    enumerate_count += 1

                    if enumerate_count % 10 == 0:
                        save_enumerate_progress(seq)
                        if enumerate_count % 100 == 0:
                            self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['enumerating_progress'].format(enumerate_count)})"))

                    self.batches = [[]]
                    self.current_batch_index = 0
                    for key in self.color_times:
                        self.color_times[key] = 0

                    all_valid = True
                    for color in seq:
                        if not self.add_color_to_sequence(color):
                            all_valid = False
                            break

                    if all_valid and len(self.get_all_colors()) == len(seq):
                        final_seq = self.get_all_colors().copy()
                        if len(final_seq) == 2:
                            final_seq = self.sort_two_color_sequence(final_seq)
                        append_enumerated_sequence(final_seq)

                if self.batch_cancelled:
                    self.body_type = old_body_type
                    self.armor_type = old_armor_type
                    self.damage_level = old_damage_level
                    self.image_size = old_image_size
                    self.batches = old_batches
                    self.color_times = old_times

                    self.load_armor_images()
                    self.load_dye_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()

                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                all_enumerated = load_enumerated_sequences()

                if not all_enumerated:
                    self.root.after(0, lambda: self.set_status(self.lang["error"].format(self.lang["no_valid_sequences"]), auto_reset=True))
                    messagebox.showinfo(self.lang["tip"], self.lang["no_valid_sequences"])

                    self.body_type = old_body_type
                    self.armor_type = old_armor_type
                    self.damage_level = old_damage_level
                    self.image_size = old_image_size
                    self.batches = old_batches
                    self.color_times = old_times

                    self.load_armor_images()
                    self.load_dye_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()

                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                if seq_len <= 2:
                    filtered_sequences = []
                    seen_signatures = set()
                    for seq in all_enumerated:
                        sig = tuple(seq)
                        if sig not in seen_signatures:
                            seen_signatures.add(sig)
                            filtered_sequences.append(seq)
                    all_sequences = filtered_sequences
                else:
                    all_sequences = all_enumerated

                save_deduped_sequences(all_sequences)
                write_progress_state('rendering', len(all_sequences), 0)

                if not all_sequences:
                    self.root.after(0, lambda: self.set_status(self.lang["error"].format(self.lang["no_valid_sequences"]), auto_reset=True))
                    messagebox.showinfo(self.lang["tip"], self.lang["no_valid_sequences"])

                    self.body_type = old_body_type
                    self.armor_type = old_armor_type
                    self.damage_level = old_damage_level
                    self.image_size = old_image_size
                    self.batches = old_batches
                    self.color_times = old_times

                    self.load_armor_images()
                    self.load_dye_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()

                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['render_start']})"))

                total = len(all_sequences)
                for idx, seq in enumerate(all_sequences):
                    if self.batch_cancelled:
                        break

                    seq_names = [self.get_english_name(c) for c in seq]
                    seq_display = ", ".join(seq_names[:3])
                    if len(seq_names) > 3:
                        seq_display += f"... (+{len(seq_names)-3})"

                    if idx % 5 == 0 or idx == total - 1:
                        self.root.after(0, lambda i=idx, t=total, s=seq_display: update_progress(i+1, t, s))
                        self.root.after(0, lambda i=idx, t=total: self.set_status(f"{self.lang['rendering']} ({i+1}/{t})"))
                        write_progress_state('rendering', total, idx)

                    try:
                        self.batches = [seq.copy()]
                        self.current_batch_index = 0
                        for key in self.color_times:
                            self.color_times[key] = 0
                        for color in seq:
                            english_name = self.get_english_name(color)
                            if english_name and english_name in self.color_times:
                                self.color_times[english_name] += 1

                        self.update_sequence_display()
                        self.update_times_display()
                        self.update_display()

                        final_img = self.render_single_image()

                        filename = self.generate_je_filename(seq, armor_type, body_type, damage_level) + ".png"
                        file_path = os.path.join(batch_output_dir, filename)
                        final_img.save(file_path, 'PNG')

                        del final_img

                        save_render_progress(seq)

                    except Exception as e:
                        print(self.lang["render_error"].format(e))

                    if (idx + 1) % 5 == 0:
                        try:
                            progress_dialog.update()
                        except:
                            pass
                        gc.collect()
                        time.sleep(0.05)

                    time.sleep(0.01)

                if not self.batch_cancelled:
                    clear_cache()
                    self.root.after(0, lambda: self.set_status(self.lang["render_complete"].format(total), auto_reset=True))
                    self.root.after(0, lambda: messagebox.showinfo(self.lang["tip"], self.lang["render_complete"].format(total)))

                self.body_type = old_body_type
                self.armor_type = old_armor_type
                self.damage_level = old_damage_level
                self.image_size = old_image_size
                self.batches = old_batches
                self.color_times = old_times

                self.load_armor_images()
                self.load_dye_images()
                self.update_sequence_display()
                self.update_times_display()
                self.update_display()

                try:
                    progress_dialog.destroy()
                except:
                    pass
                self.is_batch_rendering = False
                self.set_buttons_enabled(True)

            except Exception as e:
                try:
                    progress_dialog.destroy()
                except:
                    pass
                self.is_batch_rendering = False
                self.set_buttons_enabled(True)
                self.root.after(0, lambda: self.set_status(self.lang["error"].format(str(e)), auto_reset=True))
                messagebox.showerror(self.lang["error"], str(e))

        thread = threading.Thread(target=render_worker)
        thread.daemon = True
        thread.start()

    def batch_render_be(self, from_len, to_len, body_type, armor_type, exclude_duplicates):
        if self.is_batch_rendering:
            return

        self.is_batch_rendering = True
        self.batch_cancelled = False
        self.set_buttons_enabled(False)
        self.set_status(self.lang["rendering"])

        available_colors = [h for h, _, _ in self.color_data]

        body_str = "adult" if body_type == "adult" else "baby"
        armor_str = armor_type

        if from_len == to_len:
            folder_name = f"BE_{body_str}_{armor_str}_Len{from_len}"
        else:
            folder_name = f"BE_{body_str}_{armor_str}_Len{from_len}-{to_len}"

        batch_output_dir = os.path.join(self.output_dir, folder_name)
        if not os.path.exists(batch_output_dir):
            os.makedirs(batch_output_dir)

        cache_dir = os.path.join(self.output_dir, ".cache", folder_name)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        progress_file = os.path.join(cache_dir, "progress.txt")
        enumerated_file = os.path.join(cache_dir, "enumerated.txt")
        enumerate_progress_file = os.path.join(cache_dir, "enumerate_progress.txt")
        render_progress_file = os.path.join(cache_dir, "render_progress.txt")
        deduped_file = os.path.join(cache_dir, "deduped.txt")

        progress_dialog = tk.Toplevel(self.root)
        progress_dialog.title(self.lang["rendering"])
        progress_dialog.geometry("400x180")
        progress_dialog.transient(self.root)
        progress_dialog.protocol("WM_DELETE_WINDOW", lambda: None)

        progress_frame = ttk.Frame(progress_dialog, padding=15)
        progress_frame.pack(fill=tk.BOTH, expand=True)

        progress_label = ttk.Label(progress_frame, text=self.lang["idle"], font=("Arial", 10))
        progress_label.pack(pady=5)

        progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=350)
        progress_bar.pack(pady=10)

        status_label = ttk.Label(progress_frame, text="", font=("Arial", 8), foreground="gray")
        status_label.pack(pady=5)

        def cancel_batch():
            self.batch_cancelled = True
            self.set_status(self.lang["cancelling"], auto_reset=True)

        cancel_btn = ttk.Button(progress_frame, text=self.lang["cancel"], command=cancel_batch, width=15)
        cancel_btn.pack(pady=5)

        def update_progress(current, total, seq_info=""):
            try:
                progress_label.config(text=self.lang["render_progress"].format(current, total))
                progress_bar.config(value=(current / total) * 100 if total > 0 else 0)
                status_label.config(text=seq_info)
                progress_dialog.update()
            except:
                pass

        def read_progress_state():
            if os.path.exists(progress_file):
                try:
                    with open(progress_file, 'r', encoding='utf-8') as f:
                        data = {}
                        for line in f:
                            if '=' in line:
                                key, val = line.strip().split('=', 1)
                                data[key] = val
                        state = data.get('state', '')
                        total = int(data.get('total', 0))
                        current_index = int(data.get('current_index', 0))
                        return state, total, current_index
                except:
                    pass
            return '', 0, 0

        def write_progress_state(state, total, current_index):
            try:
                with open(progress_file, 'w', encoding='utf-8') as f:
                    f.write(f"state={state}\n")
                    f.write(f"total={total}\n")
                    f.write(f"current_index={current_index}\n")
            except:
                pass

        def append_enumerated_sequence(seq):
            try:
                with open(enumerated_file, 'a', encoding='utf-8') as f:
                    f.write(','.join(seq) + '\n')
            except:
                pass

        def load_enumerated_sequences():
            if os.path.exists(enumerated_file):
                try:
                    sequences = []
                    with open(enumerated_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                parts = line.split(',')
                                seq = [p for p in parts if p]
                                sequences.append(seq)
                    return sequences
                except:
                    pass
            return []

        def save_deduped_sequences(sequences):
            try:
                with open(deduped_file, 'w', encoding='utf-8') as f:
                    for seq in sequences:
                        f.write(','.join(seq) + '\n')
            except:
                pass

        def load_deduped_sequences():
            if os.path.exists(deduped_file):
                try:
                    sequences = []
                    with open(deduped_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                parts = line.split(',')
                                seq = [p for p in parts if p]
                                sequences.append(seq)
                    return sequences
                except:
                    pass
            return []

        def load_enumerate_progress():
            if os.path.exists(enumerate_progress_file):
                try:
                    with open(enumerate_progress_file, 'r', encoding='utf-8') as f:
                        line = f.read().strip()
                        if line:
                            return line.split(',')
                except:
                    pass
            return None

        def save_enumerate_progress(seq):
            try:
                with open(enumerate_progress_file, 'w', encoding='utf-8') as f:
                    if seq:
                        f.write(','.join(seq))
                    else:
                        f.write('')
            except:
                pass

        def load_render_progress():
            if os.path.exists(render_progress_file):
                try:
                    sequences = []
                    with open(render_progress_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                parts = line.split(',')
                                seq = [p for p in parts if p]
                                sequences.append(seq)
                    return sequences
                except:
                    pass
            return []

        def save_render_progress(seq):
            try:
                with open(render_progress_file, 'a', encoding='utf-8') as f:
                    f.write(','.join(seq) + '\n')
            except:
                pass

        def clear_cache():
            try:
                for f in [progress_file, enumerated_file, enumerate_progress_file, render_progress_file, deduped_file]:
                    if os.path.exists(f):
                        os.remove(f)
                if os.path.exists(cache_dir) and not os.listdir(cache_dir):
                    os.rmdir(cache_dir)
            except:
                pass

        def generate_sequences_with_progress(available_colors, from_len, to_len, start_length, start_seq):
            started = False if start_seq is not None else True

            for length in range(from_len, to_len + 1):
                if length < start_length:
                    continue
                elif length == start_length and start_seq is not None:
                    found_start = False
                    for seq in itertools.product(available_colors, repeat=length):
                        if not found_start:
                            if list(seq) == start_seq:
                                found_start = True
                                yield list(seq), length
                        else:
                            yield list(seq), length
                else:
                    for seq in itertools.product(available_colors, repeat=length):
                        yield list(seq), length

        def render_worker():
            try:
                old_body_type = self.body_type
                old_armor_type = self.armor_type
                old_image_size = self.image_size

                self.body_type = body_type
                self.armor_type = armor_type
                self.image_size = self.get_image_size()
                self.load_armor_images()
                self.load_dye_images()

                state, total, current_index = read_progress_state()
                deduped_sequences = load_deduped_sequences()

                if deduped_sequences:
                    state = 'rendering'
                    all_sequences = deduped_sequences
                else:
                    all_sequences = load_enumerated_sequences()

                enumerate_progress = load_enumerate_progress()
                rendered_sequences = load_render_progress()

                old_batches = copy.deepcopy(self.batches)
                old_times = self.color_times.copy()

                if state == 'rendering' and all_sequences:
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']}"))

                    start_idx = 0
                    if rendered_sequences:
                        last_rendered = rendered_sequences[-1]
                        for idx, seq in enumerate(all_sequences):
                            if seq == last_rendered:
                                start_idx = idx
                                break
                        if start_idx > 0:
                            rendered_sequences = rendered_sequences[:-1]
                            with open(render_progress_file, 'w', encoding='utf-8') as f:
                                for seq in rendered_sequences:
                                    f.write(','.join(seq) + '\n')

                    total = len(all_sequences)
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({start_idx+1}/{total})"))

                    for idx in range(start_idx, total):
                        if self.batch_cancelled:
                            break

                        seq = all_sequences[idx]
                        seq_names = [self.get_english_name(c) for c in seq]
                        seq_display = ", ".join(seq_names[:3])
                        if len(seq_names) > 3:
                            seq_display += f"... (+{len(seq_names)-3})"

                        if idx % 5 == 0 or idx == total - 1:
                            self.root.after(0, lambda i=idx, t=total, s=seq_display: update_progress(i+1, t, s))
                            self.root.after(0, lambda i=idx, t=total: self.set_status(f"{self.lang['rendering']} ({i+1}/{t})"))
                            write_progress_state('rendering', total, idx)

                        try:
                            self.batches = [seq.copy()]
                            self.current_batch_index = 0
                            for key in self.color_times:
                                self.color_times[key] = 0
                            for color in seq:
                                english_name = self.get_english_name(color)
                                if english_name and english_name in self.color_times:
                                    self.color_times[english_name] += 1

                            self.update_sequence_display()
                            self.update_times_display()
                            self.update_display()

                            final_img = self.render_single_image()

                            filename = self.generate_be_filename(seq, armor_type, body_type, "intact") + ".png"
                            file_path = os.path.join(batch_output_dir, filename)
                            final_img.save(file_path, 'PNG')

                            del final_img

                            save_render_progress(seq)

                        except Exception as e:
                            print(self.lang["render_error"].format(e))

                        if (idx + 1) % 5 == 0:
                            try:
                                progress_dialog.update()
                            except:
                                pass
                            gc.collect()
                            time.sleep(0.05)

                        time.sleep(0.01)

                    if not self.batch_cancelled:
                        clear_cache()
                        self.root.after(0, lambda: self.set_status(self.lang["render_complete"].format(total), auto_reset=True))
                        self.root.after(0, lambda: messagebox.showinfo(self.lang["tip"], self.lang["render_complete"].format(total)))

                    self.body_type = old_body_type
                    self.armor_type = old_armor_type
                    self.image_size = old_image_size
                    self.batches = old_batches
                    self.color_times = old_times

                    self.load_armor_images()
                    self.load_dye_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()

                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['enumerating']})"))

                start_length = from_len
                start_seq = None

                if enumerate_progress:
                    start_seq = enumerate_progress
                    start_length = len(start_seq)
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['resume_enumerating'].format(start_length)})"))

                enumerate_count = 0
                if all_sequences:
                    enumerate_count = len(all_sequences)
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['found_sequences'].format(enumerate_count)})"))

                seq_generator = generate_sequences_with_progress(
                    available_colors, from_len, to_len, start_length, start_seq
                )

                for seq, length in seq_generator:
                    if self.batch_cancelled:
                        break

                    enumerate_count += 1

                    if enumerate_count % 10 == 0:
                        save_enumerate_progress(seq)
                        if enumerate_count % 100 == 0:
                            self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['enumerating_progress'].format(enumerate_count)})"))

                    self.batches = [[]]
                    self.current_batch_index = 0
                    for key in self.color_times:
                        self.color_times[key] = 0

                    all_valid = True
                    for color in seq:
                        if not self.add_color_to_sequence(color):
                            all_valid = False
                            break

                    if all_valid and len(self.get_all_colors()) == len(seq):
                        final_seq = self.get_all_colors().copy()
                        if len(final_seq) == 2:
                            final_seq = self.sort_two_color_sequence(final_seq)
                        append_enumerated_sequence(final_seq)

                if self.batch_cancelled:
                    self.body_type = old_body_type
                    self.armor_type = old_armor_type
                    self.image_size = old_image_size
                    self.batches = old_batches
                    self.color_times = old_times

                    self.load_armor_images()
                    self.load_dye_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()

                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                all_enumerated = load_enumerated_sequences()

                if not all_enumerated:
                    self.root.after(0, lambda: self.set_status(self.lang["error"].format(self.lang["no_valid_sequences"]), auto_reset=True))
                    messagebox.showinfo(self.lang["tip"], self.lang["no_valid_sequences"])

                    self.body_type = old_body_type
                    self.armor_type = old_armor_type
                    self.image_size = old_image_size
                    self.batches = old_batches
                    self.color_times = old_times

                    self.load_armor_images()
                    self.load_dye_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()

                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                if exclude_duplicates:
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['deduping']})"))
                    filtered_sequences = []
                    seen_signatures = set()

                    for seq in all_enumerated:
                        if len(seq) == 2:
                            sig = tuple(sorted(seq))
                        else:
                            sig = tuple(seq)

                        if sig not in seen_signatures:
                            seen_signatures.add(sig)
                            filtered_sequences.append(seq)

                    all_sequences = filtered_sequences
                else:
                    all_sequences = all_enumerated

                save_deduped_sequences(all_sequences)
                write_progress_state('rendering', len(all_sequences), 0)

                if not all_sequences:
                    self.root.after(0, lambda: self.set_status(self.lang["error"].format(self.lang["no_valid_sequences"]), auto_reset=True))
                    messagebox.showinfo(self.lang["tip"], self.lang["no_valid_sequences"])

                    self.body_type = old_body_type
                    self.armor_type = old_armor_type
                    self.image_size = old_image_size
                    self.batches = old_batches
                    self.color_times = old_times

                    self.load_armor_images()
                    self.load_dye_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()

                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['render_start']})"))

                total = len(all_sequences)
                for idx, seq in enumerate(all_sequences):
                    if self.batch_cancelled:
                        break

                    seq_names = [self.get_english_name(c) for c in seq]
                    seq_display = ", ".join(seq_names[:3])
                    if len(seq_names) > 3:
                        seq_display += f"... (+{len(seq_names)-3})"

                    if idx % 5 == 0 or idx == total - 1:
                        self.root.after(0, lambda i=idx, t=total, s=seq_display: update_progress(i+1, t, s))
                        self.root.after(0, lambda i=idx, t=total: self.set_status(f"{self.lang['rendering']} ({i+1}/{t})"))
                        write_progress_state('rendering', total, idx)

                    try:
                        self.batches = [seq.copy()]
                        self.current_batch_index = 0
                        for key in self.color_times:
                            self.color_times[key] = 0
                        for color in seq:
                            english_name = self.get_english_name(color)
                            if english_name and english_name in self.color_times:
                                self.color_times[english_name] += 1

                        self.update_sequence_display()
                        self.update_times_display()
                        self.update_display()

                        final_img = self.render_single_image()

                        filename = self.generate_be_filename(seq, armor_type, body_type, "intact") + ".png"
                        file_path = os.path.join(batch_output_dir, filename)
                        final_img.save(file_path, 'PNG')

                        del final_img

                        save_render_progress(seq)

                    except Exception as e:
                        print(self.lang["render_error"].format(e))

                    if (idx + 1) % 5 == 0:
                        try:
                            progress_dialog.update()
                        except:
                            pass
                        gc.collect()
                        time.sleep(0.05)

                    time.sleep(0.01)

                if not self.batch_cancelled:
                    clear_cache()
                    self.root.after(0, lambda: self.set_status(self.lang["render_complete"].format(total), auto_reset=True))
                    self.root.after(0, lambda: messagebox.showinfo(self.lang["tip"], self.lang["render_complete"].format(total)))

                self.body_type = old_body_type
                self.armor_type = old_armor_type
                self.image_size = old_image_size
                self.batches = old_batches
                self.color_times = old_times

                self.load_armor_images()
                self.load_dye_images()
                self.update_sequence_display()
                self.update_times_display()
                self.update_display()

                try:
                    progress_dialog.destroy()
                except:
                    pass
                self.is_batch_rendering = False
                self.set_buttons_enabled(True)

            except Exception as e:
                try:
                    progress_dialog.destroy()
                except:
                    pass
                self.is_batch_rendering = False
                self.set_buttons_enabled(True)
                self.root.after(0, lambda: self.set_status(self.lang["error"].format(str(e)), auto_reset=True))
                messagebox.showerror(self.lang["error"], str(e))

        thread = threading.Thread(target=render_worker)
        thread.daemon = True
        thread.start()

    def batch_render_je(self, seq_len, batch_count, body_type, armor_type):
        if self.is_batch_rendering:
            return

        if seq_len <= 2:
            batch_count = 1

        self.is_batch_rendering = True
        self.batch_cancelled = False
        self.set_buttons_enabled(False)
        self.set_status(self.lang["rendering"])

        available_colors = [h for h, _, _ in self.color_data]

        body_str = "adult" if body_type == "adult" else "baby"
        armor_str = armor_type

        if seq_len <= 2:
            folder_name = f"JE_{body_str}_{armor_str}_Len{seq_len}"
        else:
            folder_name = f"JE_{body_str}_{armor_str}_Len{seq_len}_Batches{batch_count}"

        batch_output_dir = os.path.join(self.output_dir, folder_name)
        if not os.path.exists(batch_output_dir):
            os.makedirs(batch_output_dir)

        cache_dir = os.path.join(self.output_dir, ".cache", folder_name)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        progress_file = os.path.join(cache_dir, "progress.txt")
        enumerated_file = os.path.join(cache_dir, "enumerated.txt")
        enumerate_progress_file = os.path.join(cache_dir, "enumerate_progress.txt")
        render_progress_file = os.path.join(cache_dir, "render_progress.txt")
        deduped_file = os.path.join(cache_dir, "deduped.txt")

        progress_dialog = tk.Toplevel(self.root)
        progress_dialog.title(self.lang["rendering"])
        progress_dialog.geometry("400x200")
        progress_dialog.transient(self.root)
        progress_dialog.protocol("WM_DELETE_WINDOW", lambda: None)

        progress_frame = ttk.Frame(progress_dialog, padding=15)
        progress_frame.pack(fill=tk.BOTH, expand=True)

        progress_label = ttk.Label(progress_frame, text=self.lang["idle"], font=("Arial", 10))
        progress_label.pack(pady=5)

        progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=350)
        progress_bar.pack(pady=10)

        status_label = ttk.Label(progress_frame, text="", font=("Arial", 8), foreground="gray")
        status_label.pack(pady=5)

        def cancel_batch():
            self.batch_cancelled = True
            status_label.config(text=self.lang["cancelling"])

        cancel_btn = ttk.Button(progress_frame, text=self.lang["cancel"], command=cancel_batch, width=15)
        cancel_btn.pack(pady=5)

        def update_progress(current, total, seq_info=""):
            try:
                progress_label.config(text=self.lang["render_progress"].format(current, total))
                progress_bar.config(value=(current / total) * 100 if total > 0 else 0)
                status_label.config(text=seq_info)
                progress_dialog.update()
            except:
                pass

        def read_progress_state():
            if os.path.exists(progress_file):
                try:
                    with open(progress_file, 'r', encoding='utf-8') as f:
                        data = {}
                        for line in f:
                            if '=' in line:
                                key, val = line.strip().split('=', 1)
                                data[key] = val
                        state = data.get('state', '')
                        total = int(data.get('total', 0))
                        current_index = int(data.get('current_index', 0))
                        return state, total, current_index
                except:
                    pass
            return '', 0, 0

        def write_progress_state(state, total, current_index):
            try:
                with open(progress_file, 'w', encoding='utf-8') as f:
                    f.write(f"state={state}\n")
                    f.write(f"total={total}\n")
                    f.write(f"current_index={current_index}\n")
            except:
                pass

        def append_enumerated_sequence(seq):
            try:
                with open(enumerated_file, 'a', encoding='utf-8') as f:
                    f.write(','.join(seq) + '\n')
            except:
                pass

        def load_enumerated_sequences():
            if os.path.exists(enumerated_file):
                try:
                    sequences = []
                    with open(enumerated_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                parts = line.split(',')
                                seq = [p for p in parts if p]
                                sequences.append(seq)
                    return sequences
                except:
                    pass
            return []

        def save_deduped_sequences(sequences):
            try:
                with open(deduped_file, 'w', encoding='utf-8') as f:
                    for seq in sequences:
                        f.write(','.join(seq) + '\n')
            except:
                pass

        def load_deduped_sequences():
            if os.path.exists(deduped_file):
                try:
                    sequences = []
                    with open(deduped_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                parts = line.split(',')
                                seq = [p for p in parts if p]
                                sequences.append(seq)
                    return sequences
                except:
                    pass
            return []

        def load_enumerate_progress():
            if os.path.exists(enumerate_progress_file):
                try:
                    with open(enumerate_progress_file, 'r', encoding='utf-8') as f:
                        line = f.read().strip()
                        if line:
                            return line.split(',')
                except:
                    pass
            return None

        def save_enumerate_progress(seq):
            try:
                with open(enumerate_progress_file, 'w', encoding='utf-8') as f:
                    if seq:
                        f.write(','.join(seq))
                    else:
                        f.write('')
            except:
                pass

        def load_render_progress():
            if os.path.exists(render_progress_file):
                try:
                    sequences = []
                    with open(render_progress_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                parts = line.split(',')
                                seq = [p for p in parts if p]
                                sequences.append(seq)
                    return sequences
                except:
                    pass
            return []

        def save_render_progress(seq):
            try:
                with open(render_progress_file, 'a', encoding='utf-8') as f:
                    f.write(','.join(seq) + '\n')
            except:
                pass

        def clear_cache():
            try:
                for f in [progress_file, enumerated_file, enumerate_progress_file, render_progress_file, deduped_file]:
                    if os.path.exists(f):
                        os.remove(f)
                if os.path.exists(cache_dir) and not os.listdir(cache_dir):
                    os.rmdir(cache_dir)
            except:
                pass

        def generate_sequences_with_progress(available_colors, from_len, to_len, start_length, start_seq):
            for length in range(from_len, to_len + 1):
                if length < start_length:
                    continue
                elif length == start_length and start_seq is not None:
                    found_start = False
                    for seq in itertools.product(available_colors, repeat=length):
                        if not found_start:
                            if list(seq) == start_seq:
                                found_start = True
                                yield list(seq), length
                        else:
                            yield list(seq), length
                else:
                    for seq in itertools.product(available_colors, repeat=length):
                        yield list(seq), length

        def render_worker():
            try:
                old_body_type = self.body_type
                old_armor_type = self.armor_type
                old_image_size = self.image_size

                self.body_type = body_type
                self.armor_type = armor_type
                self.image_size = self.get_image_size()
                self.load_armor_images()
                self.load_dye_images()

                state, total, current_index = read_progress_state()
                deduped_sequences = load_deduped_sequences()

                if deduped_sequences:
                    state = 'rendering'
                    all_sequences = deduped_sequences
                else:
                    all_sequences = load_enumerated_sequences()

                enumerate_progress = load_enumerate_progress()
                rendered_sequences = load_render_progress()

                old_batches = copy.deepcopy(self.batches)
                old_times = self.color_times.copy()

                if state == 'rendering' and all_sequences:
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']}"))

                    start_idx = 0
                    if rendered_sequences:
                        last_rendered = rendered_sequences[-1]
                        for idx, seq in enumerate(all_sequences):
                            if seq == last_rendered:
                                start_idx = idx
                                break
                        if start_idx > 0:
                            rendered_sequences = rendered_sequences[:-1]
                            with open(render_progress_file, 'w', encoding='utf-8') as f:
                                for seq in rendered_sequences:
                                    f.write(','.join(seq) + '\n')

                    total = len(all_sequences)
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({start_idx+1}/{total})"))

                    for idx in range(start_idx, total):
                        if self.batch_cancelled:
                            break

                        seq = all_sequences[idx]
                        seq_names = [self.get_english_name(c) for c in seq]
                        seq_display = ", ".join(seq_names[:3])
                        if len(seq_names) > 3:
                            seq_display += f"... (+{len(seq_names)-3})"

                        if idx % 5 == 0 or idx == total - 1:
                            self.root.after(0, lambda i=idx, t=total, s=seq_display: update_progress(i+1, t, s))
                            self.root.after(0, lambda i=idx, t=total: self.set_status(f"{self.lang['rendering']} ({i+1}/{t})"))
                            write_progress_state('rendering', total, idx)

                        try:
                            self.batches = [seq.copy()]
                            self.current_batch_index = 0
                            for key in self.color_times:
                                self.color_times[key] = 0
                            for color in seq:
                                english_name = self.get_english_name(color)
                                if english_name and english_name in self.color_times:
                                    self.color_times[english_name] += 1

                            self.update_sequence_display()
                            self.update_times_display()
                            self.update_display()

                            final_img = self.render_single_image()

                            filename = self.generate_je_filename(seq, armor_type, body_type, "intact") + ".png"
                            file_path = os.path.join(batch_output_dir, filename)
                            final_img.save(file_path, 'PNG')

                            del final_img

                            save_render_progress(seq)

                        except Exception as e:
                            print(self.lang["render_error"].format(e))

                        if (idx + 1) % 5 == 0:
                            try:
                                progress_dialog.update()
                            except:
                                pass
                            gc.collect()
                            time.sleep(0.05)

                        time.sleep(0.01)

                    if not self.batch_cancelled:
                        clear_cache()
                        self.root.after(0, lambda: self.set_status(self.lang["render_complete"].format(total), auto_reset=True))
                        self.root.after(0, lambda: messagebox.showinfo(self.lang["tip"], self.lang["render_complete"].format(total)))

                    self.body_type = old_body_type
                    self.armor_type = old_armor_type
                    self.image_size = old_image_size
                    self.batches = old_batches
                    self.color_times = old_times

                    self.load_armor_images()
                    self.load_dye_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()

                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['enumerating']})"))

                start_length = seq_len if seq_len <= 2 else 1
                start_seq = None

                if enumerate_progress:
                    start_seq = enumerate_progress
                    start_length = len(start_seq)
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['resume_enumerating'].format(start_length)})"))

                enumerate_count = 0
                if all_sequences:
                    enumerate_count = len(all_sequences)
                    self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['found_sequences'].format(enumerate_count)})"))

                seq_generator = generate_sequences_with_progress(
                    available_colors, seq_len, seq_len, start_length, start_seq
                )

                for seq, length in seq_generator:
                    if self.batch_cancelled:
                        break

                    enumerate_count += 1

                    if enumerate_count % 10 == 0:
                        save_enumerate_progress(seq)
                        if enumerate_count % 100 == 0:
                            self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['enumerating_progress'].format(enumerate_count)})"))

                    self.batches = [[]]
                    self.current_batch_index = 0
                    for key in self.color_times:
                        self.color_times[key] = 0

                    all_valid = True
                    for color in seq:
                        if not self.add_color_to_sequence(color):
                            all_valid = False
                            break

                    if all_valid and len(self.get_all_colors()) == len(seq):
                        final_seq = self.get_all_colors().copy()
                        if len(final_seq) == 2:
                            final_seq = self.sort_two_color_sequence(final_seq)
                        append_enumerated_sequence(final_seq)

                if self.batch_cancelled:
                    self.body_type = old_body_type
                    self.armor_type = old_armor_type
                    self.image_size = old_image_size
                    self.batches = old_batches
                    self.color_times = old_times

                    self.load_armor_images()
                    self.load_dye_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()

                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                all_enumerated = load_enumerated_sequences()

                if not all_enumerated:
                    self.root.after(0, lambda: self.set_status(self.lang["error"].format(self.lang["no_valid_sequences"]), auto_reset=True))
                    messagebox.showinfo(self.lang["tip"], self.lang["no_valid_sequences"])

                    self.body_type = old_body_type
                    self.armor_type = old_armor_type
                    self.image_size = old_image_size
                    self.batches = old_batches
                    self.color_times = old_times

                    self.load_armor_images()
                    self.load_dye_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()

                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                if seq_len <= 2:
                    filtered_sequences = []
                    seen_signatures = set()
                    for seq in all_enumerated:
                        sig = tuple(seq)
                        if sig not in seen_signatures:
                            seen_signatures.add(sig)
                            filtered_sequences.append(seq)
                    all_sequences = filtered_sequences
                else:
                    all_sequences = all_enumerated

                save_deduped_sequences(all_sequences)
                write_progress_state('rendering', len(all_sequences), 0)

                if not all_sequences:
                    self.root.after(0, lambda: self.set_status(self.lang["error"].format(self.lang["no_valid_sequences"]), auto_reset=True))
                    messagebox.showinfo(self.lang["tip"], self.lang["no_valid_sequences"])

                    self.body_type = old_body_type
                    self.armor_type = old_armor_type
                    self.image_size = old_image_size
                    self.batches = old_batches
                    self.color_times = old_times

                    self.load_armor_images()
                    self.load_dye_images()
                    self.update_sequence_display()
                    self.update_times_display()
                    self.update_display()

                    try:
                        progress_dialog.destroy()
                    except:
                        pass
                    self.is_batch_rendering = False
                    self.set_buttons_enabled(True)
                    return

                self.root.after(0, lambda: self.set_status(f"{self.lang['rendering']} ({self.lang['render_start']})"))

                total = len(all_sequences)
                for idx, seq in enumerate(all_sequences):
                    if self.batch_cancelled:
                        break

                    seq_names = [self.get_english_name(c) for c in seq]
                    seq_display = ", ".join(seq_names[:3])
                    if len(seq_names) > 3:
                        seq_display += f"... (+{len(seq_names)-3})"

                    if idx % 5 == 0 or idx == total - 1:
                        self.root.after(0, lambda i=idx, t=total, s=seq_display: update_progress(i+1, t, s))
                        self.root.after(0, lambda i=idx, t=total: self.set_status(f"{self.lang['rendering']} ({i+1}/{t})"))
                        write_progress_state('rendering', total, idx)

                    try:
                        self.batches = [seq.copy()]
                        self.current_batch_index = 0
                        for key in self.color_times:
                            self.color_times[key] = 0
                        for color in seq:
                            english_name = self.get_english_name(color)
                            if english_name and english_name in self.color_times:
                                self.color_times[english_name] += 1

                        self.update_sequence_display()
                        self.update_times_display()
                        self.update_display()

                        final_img = self.render_single_image()

                        filename = self.generate_je_filename(seq, armor_type, body_type, "intact") + ".png"
                        file_path = os.path.join(batch_output_dir, filename)
                        final_img.save(file_path, 'PNG')

                        del final_img

                        save_render_progress(seq)

                    except Exception as e:
                        print(self.lang["render_error"].format(e))

                    if (idx + 1) % 5 == 0:
                        try:
                            progress_dialog.update()
                        except:
                            pass
                        gc.collect()
                        time.sleep(0.05)

                    time.sleep(0.01)

                if not self.batch_cancelled:
                    clear_cache()
                    self.root.after(0, lambda: self.set_status(self.lang["render_complete"].format(total), auto_reset=True))
                    self.root.after(0, lambda: messagebox.showinfo(self.lang["tip"], self.lang["render_complete"].format(total)))

                self.body_type = old_body_type
                self.armor_type = old_armor_type
                self.image_size = old_image_size
                self.batches = old_batches
                self.color_times = old_times

                self.load_armor_images()
                self.load_dye_images()
                self.update_sequence_display()
                self.update_times_display()
                self.update_display()

                try:
                    progress_dialog.destroy()
                except:
                    pass
                self.is_batch_rendering = False
                self.set_buttons_enabled(True)

            except Exception as e:
                try:
                    progress_dialog.destroy()
                except:
                    pass
                self.is_batch_rendering = False
                self.set_buttons_enabled(True)
                self.root.after(0, lambda: self.set_status(self.lang["error"].format(str(e)), auto_reset=True))
                messagebox.showerror(self.lang["error"], str(e))

        thread = threading.Thread(target=render_worker)
        thread.daemon = True
        thread.start()

    def generate_be_filename(self, seq, armor_type, body_type, damage_level):
        if not seq:
            if armor_type == "wolf_armor":
                damage_str = {
                    "intact": "durability_61-64",
                    "slightly_damaged": "durability_45-60",
                    "moderately_damaged": "durability_21-44",
                    "very_damaged": "durability_1-20"
                }.get(damage_level, "durability_61-64")
                return f"Wolf_Armor_({damage_str})_BE2"
            elif armor_type == "horse_armor":
                return f"Leather_Horse_Armor_BE3"
            else:
                if body_type == "adult":
                    return f"Leather_{armor_type.capitalize()}_BE2"
                else:
                    return f"Leather_{armor_type.capitalize()}_BE1"

        valid_seq = []
        temp_color = self.hex_to_rgb(self.default_color)
        for color in seq:
            r, g, b = self.hex_to_rgb(color)
            new_color = ((temp_color[0] + r) // 2, (temp_color[1] + g) // 2, (temp_color[2] + b) // 2)
            if new_color != temp_color:
                valid_seq.append(color)
                temp_color = new_color

        if not valid_seq:
            if armor_type == "wolf_armor":
                damage_str = {
                    "intact": "durability_61-64",
                    "slightly_damaged": "durability_45-60",
                    "moderately_damaged": "durability_21-44",
                    "very_damaged": "durability_1-20"
                }.get(damage_level, "durability_61-64")
                return f"Wolf_Armor_({damage_str})_BE2"
            elif armor_type == "horse_armor":
                return f"Leather_Horse_Armor_BE3"
            else:
                if body_type == "adult":
                    return f"Leather_{armor_type.capitalize()}_BE2"
                else:
                    return f"Leather_{armor_type.capitalize()}_BE1"

        if len(valid_seq) == 1:
            english_name = self.get_english_name(valid_seq[0])
            full_name = self.get_color_full_name(english_name)
            if armor_type == "wolf_armor":
                damage_str = {
                    "intact": "durability_61-64",
                    "slightly_damaged": "durability_45-60",
                    "moderately_damaged": "durability_21-44",
                    "very_damaged": "durability_1-20"
                }.get(damage_level, "durability_61-64")
                return f"{full_name}_Wolf_Armor_({damage_str})_BE2"
            elif armor_type == "horse_armor":
                return f"{full_name}_Leather_Horse_Armor_BE3"
            else:
                if body_type == "adult":
                    return f"{full_name}_Leather_{armor_type.capitalize()}_BE2"
                else:
                    return f"{full_name}_Leather_{armor_type.capitalize()}_BE1"

        if len(valid_seq) == 2:
            valid_seq = self.sort_two_color_sequence(valid_seq)

        abbr_parts = []
        i = 0
        while i < len(valid_seq):
            current_color = valid_seq[i]
            english_name = self.get_english_name(current_color)
            abbr = self.get_color_abbr(english_name)
            count = 1
            while i + count < len(valid_seq) and valid_seq[i + count] == current_color:
                count += 1
            if count == 1:
                abbr_parts.append(abbr)
            else:
                abbr_parts.append(f"{count}{abbr}")
            i += count

        abbr_string = "-".join(abbr_parts)

        if armor_type == "wolf_armor":
            damage_str = {
                "intact": "durability_61-64",
                "slightly_damaged": "durability_45-60",
                "moderately_damaged": "durability_21-44",
                "very_damaged": "durability_1-20"
            }.get(damage_level, "durability_61-64")
            return f"{abbr_string}_Wolf_Armor_({damage_str})_BE2"
        elif armor_type == "horse_armor":
            return f"{abbr_string}_Leather_Horse_Armor_BE3"
        else:
            if body_type == "adult":
                return f"{abbr_string}_Leather_{armor_type.capitalize()}_BE2"
            else:
                return f"{abbr_string}_Leather_{armor_type.capitalize()}_BE1"

    def generate_je_filename(self, seq, armor_type, body_type, damage_level):
        if not seq:
            if armor_type == "wolf_armor":
                damage_str = {
                    "intact": "durability_61-64",
                    "slightly_damaged": "durability_45-60",
                    "moderately_damaged": "durability_21-44",
                    "very_damaged": "durability_1-20"
                }.get(damage_level, "durability_61-64")
                return f"Wolf_Armor_({damage_str})_JE2"
            elif armor_type == "horse_armor":
                return f"Leather_Horse_Armor_JE2"
            else:
                if body_type == "adult":
                    return f"Leather_{armor_type.capitalize()}_JE4"
                else:
                    return f"Leather_{armor_type.capitalize()}_JE1"

        all_colors = []
        for batch in self.batches:
            all_colors.extend(batch)

        valid_seq = []
        temp_color = self.hex_to_rgb(self.default_color)
        for color in all_colors:
            r, g, b = self.hex_to_rgb(color)
            new_color = ((temp_color[0] + r) // 2, (temp_color[1] + g) // 2, (temp_color[2] + b) // 2)
            if new_color != temp_color:
                valid_seq.append(color)
                temp_color = new_color

        if not valid_seq:
            if armor_type == "wolf_armor":
                damage_str = {
                    "intact": "durability_61-64",
                    "slightly_damaged": "durability_45-60",
                    "moderately_damaged": "durability_21-44",
                    "very_damaged": "durability_1-20"
                }.get(damage_level, "durability_61-64")
                return f"Wolf_Armor_({damage_str})_JE2"
            elif armor_type == "horse_armor":
                return f"Leather_Horse_Armor_JE2"
            else:
                if body_type == "adult":
                    return f"Leather_{armor_type.capitalize()}_JE4"
                else:
                    return f"Leather_{armor_type.capitalize()}_JE1"

        if len(valid_seq) == 1:
            english_name = self.get_english_name(valid_seq[0])
            full_name = self.get_color_full_name(english_name)
            if armor_type == "wolf_armor":
                damage_str = {
                    "intact": "durability_61-64",
                    "slightly_damaged": "durability_45-60",
                    "moderately_damaged": "durability_21-44",
                    "very_damaged": "durability_1-20"
                }.get(damage_level, "durability_61-64")
                return f"{full_name}_Wolf_Armor_({damage_str})_JE2"
            elif armor_type == "horse_armor":
                return f"{full_name}_Leather_Horse_Armor_JE2"
            else:
                if body_type == "adult":
                    return f"{full_name}_Leather_{armor_type.capitalize()}_JE4"
                else:
                    return f"{full_name}_Leather_{armor_type.capitalize()}_JE1"

        if len(valid_seq) == 2:
            valid_seq = self.sort_two_color_sequence(valid_seq)
            abbr_parts = []
            for color in valid_seq:
                english_name = self.get_english_name(color)
                abbr = self.get_color_abbr(english_name)
                abbr_parts.append(abbr)
            abbr_string = "-".join(abbr_parts)
            if armor_type == "wolf_armor":
                damage_str = {
                    "intact": "durability_61-64",
                    "slightly_damaged": "durability_45-60",
                    "moderately_damaged": "durability_21-44",
                    "very_damaged": "durability_1-20"
                }.get(damage_level, "durability_61-64")
                return f"{abbr_string}_Wolf_Armor_({damage_str})_JE2"
            elif armor_type == "horse_armor":
                return f"{abbr_string}_Leather_Horse_Armor_JE2"
            else:
                if body_type == "adult":
                    return f"{abbr_string}_Leather_{armor_type.capitalize()}_JE4"
                else:
                    return f"{abbr_string}_Leather_{armor_type.capitalize()}_JE1"

        batch_parts = []
        for batch_idx, batch in enumerate(self.batches):
            if not batch:
                continue
            color_counts = {}
            for color in batch:
                english_name = self.get_english_name(color)
                if english_name:
                    color_counts[english_name] = color_counts.get(english_name, 0) + 1
            batch_entries = []
            for color_name in self.color_order:
                internal_name = color_name.lower()
                if internal_name in color_counts:
                    abbr = self.get_color_abbr(internal_name)
                    count = color_counts[internal_name]
                    batch_entries.append(f"{abbr}-{count}")
            if batch_entries:
                batch_parts.append("_".join(batch_entries))

        if not batch_parts:
            if armor_type == "wolf_armor":
                damage_str = {
                    "intact": "durability_61-64",
                    "slightly_damaged": "durability_45-60",
                    "moderately_damaged": "durability_21-44",
                    "very_damaged": "durability_1-20"
                }.get(damage_level, "durability_61-64")
                return f"Wolf_Armor_({damage_str})_JE2"
            elif armor_type == "horse_armor":
                return f"Leather_Horse_Armor_JE2"
            else:
                if body_type == "adult":
                    return f"Leather_{armor_type.capitalize()}_JE4"
                else:
                    return f"Leather_{armor_type.capitalize()}_JE1"

        prefix = "&".join(batch_parts)

        if armor_type == "wolf_armor":
            damage_str = {
                "intact": "durability_61-64",
                "slightly_damaged": "durability_45-60",
                "moderately_damaged": "durability_21-44",
                "very_damaged": "durability_1-20"
            }.get(damage_level, "durability_61-64")
            return f"{prefix}_Wolf_Armor_({damage_str})_JE2"
        elif armor_type == "horse_armor":
            return f"{prefix}_Leather_Horse_Armor_JE2"
        else:
            if body_type == "adult":
                return f"{prefix}_Leather_{armor_type.capitalize()}_JE4"
            else:
                return f"{prefix}_Leather_{armor_type.capitalize()}_JE1"

    def generate_filename(self):
        if self.game_version == "BE":
            return self.generate_be_filename(self.get_all_colors(), self.armor_type, self.body_type, self.damage_level)
        else:
            return self.generate_je_filename(self.get_all_colors(), self.armor_type, self.body_type, self.damage_level)

    def render_single_image(self):
        if not self.images:
            return Image.new('RGBA', self.image_size, (0, 0, 0, 0))

        if self.armor_type == "wolf_armor":
            if self.background_image is not None:
                d_layer = self.background_image.copy()
                if d_layer.size != self.image_size:
                    d_layer = self.resize_image(d_layer, self.image_size[0], self.image_size[1])
            else:
                d_layer = Image.new('RGBA', self.image_size, (0, 0, 0, 0))
            
            if self.images and len(self.images) > 0:
                u_layer = self.images[0].copy()
                if u_layer.size != self.image_size:
                    u_layer = self.resize_image(u_layer, self.image_size[0], self.image_size[1])
            else:
                u_layer = Image.new('RGBA', self.image_size, (0, 0, 0, 0))
            
            all_colors = self.get_all_colors()
            has_dye = len(all_colors) > 0
            
            if has_dye:
                blend_color = self.calculate_blend_color()
                
                r_channel, g_channel, b_channel, a_channel = u_layer.split()
                r_array = np.array(r_channel, dtype=np.float32)
                g_array = np.array(g_channel, dtype=np.float32)
                b_array = np.array(b_channel, dtype=np.float32)
                a_array = np.array(a_channel, dtype=np.float32)
                
                blend_r, blend_g, blend_b = blend_color
                
                result_r = (r_array * blend_r) / 255.0
                result_g = (g_array * blend_g) / 255.0
                result_b = (b_array * blend_b) / 255.0
                result_a = a_array
                
                result_r_clipped = np.clip(result_r, 0, 255).astype(np.uint8)
                result_g_clipped = np.clip(result_g, 0, 255).astype(np.uint8)
                result_b_clipped = np.clip(result_b, 0, 255).astype(np.uint8)
                result_a_clipped = result_a.astype(np.uint8)
                
                colored_u = Image.merge('RGBA', (
                    Image.fromarray(result_r_clipped),
                    Image.fromarray(result_g_clipped),
                    Image.fromarray(result_b_clipped),
                    Image.fromarray(result_a_clipped)
                ))
                
                final_img = Image.alpha_composite(d_layer, colored_u)
            else:
                final_img = d_layer
            
            return final_img
        
        else:
            original_img = self.images[0].copy()
            if original_img.size != self.image_size:
                original_img = self.resize_image(original_img, self.image_size[0], self.image_size[1])

            blend_color = self.calculate_blend_color()

            fg_r, fg_g, fg_b, fg_a, original_a = self.blend_images_float(original_img, blend_color)
            if fg_r is None:
                return original_img

            fg_r_clipped = np.clip(fg_r, 0, 255).astype(np.uint8)
            fg_g_clipped = np.clip(fg_g, 0, 255).astype(np.uint8)
            fg_b_clipped = np.clip(fg_b, 0, 255).astype(np.uint8)
            fg_a_clipped = fg_a.astype(np.uint8)

            blended_img = Image.merge('RGBA', (
                Image.fromarray(fg_r_clipped),
                Image.fromarray(fg_g_clipped),
                Image.fromarray(fg_b_clipped),
                Image.fromarray(fg_a_clipped)
            ))

            if self.overlay_image is not None:
                if self.overlay_image.size != self.image_size:
                    overlay = self.resize_image(self.overlay_image, self.image_size[0], self.image_size[1])
                else:
                    overlay = self.overlay_image.copy()
                blended_img = Image.alpha_composite(blended_img, overlay)

            return blended_img

    def blend_images_float(self, original_img, blend_color):
        try:
            if original_img.size != self.image_size:
                original_img = self.resize_image(original_img, self.image_size[0], self.image_size[1])

            r_channel, g_channel, b_channel, a_channel = original_img.split()

            r_array = np.array(r_channel, dtype=np.float32)
            g_array = np.array(g_channel, dtype=np.float32)
            b_array = np.array(b_channel, dtype=np.float32)
            a_array = np.array(a_channel, dtype=np.float32)

            blend_r, blend_g, blend_b = blend_color

            result_r = (r_array * blend_r) / 255.0
            result_g = (g_array * blend_g) / 255.0
            result_b = (b_array * blend_b) / 255.0
            result_a = a_array

            return result_r, result_g, result_b, result_a, a_array
        except Exception:
            return None, None, None, None, None

    def change_language(self, lang_code):
        if lang_code in LANGUAGES:
            self.current_lang = lang_code
            self.lang = LANGUAGES[lang_code]
            self.root.title(self.lang["title"])

            for code, frame in self.lang_tab_frames.items():
                if code == lang_code:
                    self.right_content = frame
                    break

            self.rebuild_content()
            self.update_all_texts()
            self.update_color_display()
            self.update_display()
            self.update_times_display()
            self.update_sequence_display()

    def rebuild_content(self):
        for widget in self.right_content.winfo_children():
            widget.destroy()

        self.status_label = ttk.LabelFrame(self.right_content, text=self.lang["current_status"])
        self.status_label.pack(pady=5, fill=tk.X)

        status_inner = ttk.Frame(self.status_label)
        status_inner.pack(pady=5, padx=10)

        self.version_label = ttk.Label(status_inner, text=self.lang["version"], font=("Arial", 10, "bold"))
        self.version_label.pack(side=tk.LEFT, padx=5)
        self.version_display = ttk.Label(status_inner, text=self.game_version, font=("Arial", 10), foreground="blue")
        self.version_display.pack(side=tk.LEFT, padx=5)

        ttk.Separator(status_inner, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.armor_label = ttk.Label(status_inner, text=self.lang["armor_type"], font=("Arial", 10, "bold"))
        self.armor_label.pack(side=tk.LEFT, padx=5)
        
        if self.armor_type == "horse_armor":
            armor_display_name = self.lang["horse_armor"]
            self.armor_display = ttk.Label(status_inner, text=armor_display_name, font=("Arial", 10), foreground="orange")
        elif self.armor_type == "wolf_armor":
            armor_display_name = self.lang["wolf_armor"]
            self.armor_display = ttk.Label(status_inner, text=armor_display_name, font=("Arial", 10), foreground="#C67B30")
        else:
            armor_display_name = {
                "helmet": self.lang["helmet"],
                "chestplate": self.lang["chestplate"],
                "leggings": self.lang["leggings"],
                "boots": self.lang["boots"]
            }.get(self.armor_type, self.armor_type)
            self.armor_display = ttk.Label(status_inner, text=armor_display_name, font=("Arial", 10), foreground="green")
        self.armor_display.pack(side=tk.LEFT, padx=5)

        ttk.Separator(status_inner, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.body_label = ttk.Label(status_inner, text=self.lang["body_type"], font=("Arial", 10, "bold"))
        self.body_label.pack(side=tk.LEFT, padx=5)
        if self.armor_type == "horse_armor" or self.armor_type == "wolf_armor":
            body_display_name = "N/A"
            self.body_display = ttk.Label(status_inner, text=body_display_name, font=("Arial", 10), foreground="gray")
        else:
            body_display_name = {
                "adult": self.lang["adult"],
                "baby": self.lang["baby"]
            }.get(self.body_type, self.body_type)
            self.body_display = ttk.Label(status_inner, text=body_display_name, font=("Arial", 10), foreground="purple")
        self.body_display.pack(side=tk.LEFT, padx=5)

        if self.armor_type == "wolf_armor":
            ttk.Separator(status_inner, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=10)
            self.damage_label = ttk.Label(status_inner, text=self.lang["damage_level"], font=("Arial", 10, "bold"))
            self.damage_label.pack(side=tk.LEFT, padx=5)
            damage_display_name = {
                "intact": self.lang["intact"],
                "slightly_damaged": self.lang["slightly_damaged"],
                "moderately_damaged": self.lang["moderately_damaged"],
                "very_damaged": self.lang["very_damaged"]
            }.get(self.damage_level, self.damage_level)
            self.damage_display = ttk.Label(status_inner, text=damage_display_name, font=("Arial", 10), foreground="#C67B30")
            self.damage_display.pack(side=tk.LEFT, padx=5)

        version_title_frame = ttk.Frame(self.right_content)
        version_title_frame.pack(pady=(0, 5))
        self.version_title_label = ttk.Label(version_title_frame, text=self.lang["version"], font=("Arial", 11, "bold"))
        self.version_title_label.pack()

        version_frame = ttk.Frame(self.right_content)
        version_frame.pack(pady=5)

        for v in ["JE", "BE"]:
            btn = ttk.Button(
                version_frame,
                text=v,
                command=lambda val=v: self.select_version(val),
                width=8
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.all_buttons.append(btn)

        body_title_frame = ttk.Frame(self.right_content)
        body_title_frame.pack(pady=(0, 5))
        self.body_title_label = ttk.Label(body_title_frame, text=self.lang["body_type"], font=("Arial", 11, "bold"))
        self.body_title_label.pack()

        body_frame = ttk.Frame(self.right_content)
        body_frame.pack(pady=5)

        self.body_btns = []
        for body in ["adult", "baby"]:
            display_name = self.lang["adult"] if body == "adult" else self.lang["baby"]
            btn = ttk.Button(
                body_frame,
                text=display_name,
                command=lambda val=body: self.select_body_type(val),
                width=8
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.all_buttons.append(btn)
            self.body_btns.append(btn)

        if self.armor_type == "horse_armor" or self.armor_type == "wolf_armor":
            for btn in self.body_btns:
                btn.config(state='disabled')

        damage_title_frame = ttk.Frame(self.right_content)
        damage_title_frame.pack(pady=(0, 5))
        self.damage_title_label = ttk.Label(damage_title_frame, text=self.lang["damage_level"], font=("Arial", 11, "bold"))
        self.damage_title_label.pack()

        damage_frame = ttk.Frame(self.right_content)
        damage_frame.pack(pady=5)

        self.damage_btns = []
        damage_levels = ["intact", "slightly_damaged", "moderately_damaged", "very_damaged"]
        damage_display = {
            "intact": self.lang["intact"],
            "slightly_damaged": self.lang["slightly_damaged"],
            "moderately_damaged": self.lang["moderately_damaged"],
            "very_damaged": self.lang["very_damaged"]
        }
        
        for level in damage_levels:
            btn = ttk.Button(
                damage_frame,
                text=damage_display[level],
                command=lambda val=level: self.select_damage_level(val),
                width=10
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.all_buttons.append(btn)
            self.damage_btns.append(btn)
        
        if self.armor_type != "wolf_armor":
            for btn in self.damage_btns:
                btn.config(state='disabled')

        armor_title_frame = ttk.Frame(self.right_content)
        armor_title_frame.pack(pady=(0, 5))
        self.armor_title_label = ttk.Label(armor_title_frame, text=self.lang["armor_type"], font=("Arial", 11, "bold"))
        self.armor_title_label.pack()

        armor_frame = ttk.Frame(self.right_content)
        armor_frame.pack(pady=5)

        for armor in ["helmet", "chestplate", "leggings", "boots", "horse_armor", "wolf_armor"]:
            display_name = {
                "helmet": self.lang["helmet"],
                "chestplate": self.lang["chestplate"],
                "leggings": self.lang["leggings"],
                "boots": self.lang["boots"],
                "horse_armor": self.lang["horse_armor"],
                "wolf_armor": self.lang["wolf_armor"]
            }.get(armor, armor)
            btn = ttk.Button(
                armor_frame,
                text=display_name,
                command=lambda val=armor: self.select_armor_type(val),
                width=10
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.all_buttons.append(btn)

        ttk.Separator(self.right_content, orient='horizontal').pack(fill=tk.X, pady=10)

        self.color_display_frame = ttk.Frame(self.right_content)
        self.color_display_frame.pack(pady=5, fill=tk.X)

        self.color_display_label = ttk.Label(self.color_display_frame, text=self.lang["current_blend"], font=("Arial", 9))
        self.current_color_preview = tk.Canvas(self.color_display_frame, width=25, height=18,
                                               bg='white', relief='solid', borderwidth=1)
        self.current_color_label = ttk.Label(self.color_display_frame, text="#FFFFFF", font=("Arial", 8))

        self.target_prefix_label = ttk.Label(self.color_display_frame, text=self.lang["target_color"], font=("Arial", 9))
        self.target_color_preview = tk.Canvas(self.color_display_frame, width=25, height=18,
                                              bg='white', relief='solid', borderwidth=1, cursor="hand2")
        self.target_color_preview.bind('<Button-1>', lambda e: self.pick_target_color())
        self.target_color_label = ttk.Label(self.color_display_frame, text="#FFFFFF", font=("Arial", 8))

        self.delta_prefix_label = ttk.Label(self.color_display_frame, text=self.lang["delta_e"], font=("Arial", 9, "bold"))
        self.delta_e_label = ttk.Label(self.color_display_frame, text="0.00", font=("Arial", 9, "bold"), foreground="green")

        self.placeholder_label = ttk.Label(self.color_display_frame,
                                           text=self.lang["no_dye"],
                                           font=("Arial", 10), foreground="gray")

        self.batch_count_label = ttk.Label(self.color_display_frame, text=f"{self.lang['batch']}: 1",
                                           font=("Arial", 10), foreground="gray")
        self.batch_count_label.pack(side=tk.RIGHT, padx=5)

        self.color_display_label.pack_forget()
        self.current_color_preview.pack_forget()
        self.current_color_label.pack_forget()
        self.target_prefix_label.pack_forget()
        self.target_color_preview.pack_forget()
        self.target_color_label.pack_forget()
        self.delta_prefix_label.pack_forget()
        self.delta_e_label.pack_forget()
        self.placeholder_label.pack(side=tk.LEFT, padx=5)

        self.auto_frame = ttk.Frame(self.right_content)
        self.auto_frame.pack(pady=5, fill=tk.X)

        self.auto_gen_btn = ttk.Button(self.auto_frame, text=self.lang["calc_sequence"],
                                       command=self.auto_generate_sequence, width=20)
        self.auto_gen_btn.pack(side=tk.LEFT, padx=5)
        self.all_buttons.append(self.auto_gen_btn)

        self.based_on_label = ttk.Label(self.auto_frame, text=self.lang["based_on"], font=("Arial", 8), foreground="gray")
        self.based_on_label.pack(side=tk.LEFT, padx=5)

        self.new_batch_btn = ttk.Button(self.auto_frame, text=self.lang["new_batch"],
                                        command=self.add_new_batch, width=12)
        if self.game_version == "BE":
            self.new_batch_btn.pack_forget()
        else:
            self.new_batch_btn.pack(side=tk.RIGHT, padx=5)
        self.all_buttons.append(self.new_batch_btn)

        self.batch_render_btn = ttk.Button(self.auto_frame, text=self.lang["batch_render"],
                                           command=self.open_batch_render_dialog, width=12)
        self.batch_render_btn.pack(side=tk.RIGHT, padx=5)
        self.all_buttons.append(self.batch_render_btn)

        self.sequence_frame = ttk.LabelFrame(self.right_content, text=self.lang["sequence"])
        self.sequence_frame.pack(pady=5, fill=tk.BOTH, expand=True)

        list_container = ttk.Frame(self.sequence_frame)
        list_container.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        self.list_canvas = tk.Canvas(list_container, height=100, bg='white', highlightthickness=1, highlightcolor='gray')
        self.list_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.list_canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.list_canvas.configure(yscrollcommand=scrollbar.set)

        self.list_inner = tk.Frame(self.list_canvas, bg='white')
        self.list_canvas_window = self.list_canvas.create_window((0, 0), window=self.list_inner, anchor=tk.NW)

        self.list_items = []
        self.batch_labels = []

        self.list_canvas.bind('<Configure>', self.on_canvas_configure)
        self.list_inner.bind('<Configure>', self.on_inner_configure)

        seq_control_frame = ttk.Frame(self.sequence_frame)
        seq_control_frame.pack(pady=5)

        self.clear_btn = ttk.Button(seq_control_frame, text=self.lang["clear"], command=self.clear_sequence, width=12)
        self.clear_btn.pack(side=tk.LEFT, padx=3)
        self.all_buttons.append(self.clear_btn)

        self.times_frame = ttk.LabelFrame(self.right_content, text=self.lang["dye_times"])
        self.times_frame.pack(pady=5, fill=tk.X)

        self.times_labels = {}
        times_inner = ttk.Frame(self.times_frame)
        times_inner.pack(pady=5, padx=5, fill=tk.X)

        for i, (hex_val, chinese_name, english_name) in enumerate(self.color_data):
            row = i // 8
            col = i % 8
            frame = ttk.Frame(times_inner)
            frame.grid(row=row, column=col, padx=2, pady=1, sticky='w')

            r, g, b = self.hex_to_rgb(hex_val)
            color_hex = f'#{r:02x}{g:02x}{b:02x}'
            square = tk.Canvas(frame, width=10, height=10, bg=color_hex, highlightthickness=0)
            square.pack(side=tk.LEFT)

            label = tk.Label(frame, text=f"{chinese_name}:0", font=("Arial", 8), bg='#f0f0f0')
            label.pack(side=tk.LEFT, padx=2)
            self.times_labels[english_name] = label

        for i in range(8):
            times_inner.grid_columnconfigure(i, weight=1)

        self.quick_frame = ttk.LabelFrame(self.right_content, text=self.lang["dye_options"])
        self.quick_frame.pack(pady=5, fill=tk.X)

        self.dye_buttons = []
        self.dye_icon_labels = []
        for i, (hex_val, chinese_name, english_name) in enumerate(self.color_data):
            row = i // 4
            col = i % 4

            btn_frame = tk.Frame(self.quick_frame, bg='#f0f0f0', relief='raised', bd=1)
            btn_frame.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')

            img = self.dye_images.get(hex_val)
            if img:
                icon_label = tk.Label(btn_frame, image=img, bg='#f0f0f0', width=16, height=16)
            else:
                icon_label = tk.Label(btn_frame, text='■', font=('Arial', 10), bg='#f0f0f0', width=2, height=1)
            icon_label.pack(pady=(2, 0))
            self.dye_icon_labels.append(icon_label)

            display_name = self.get_display_color_name(english_name)
            text_label = tk.Label(btn_frame, text=display_name, font=('Arial', 8), bg='#f0f0f0')
            text_label.pack(pady=(0, 2))

            def make_on_click(h):
                return lambda e: self.add_color_to_sequence(h)

            btn_frame.bind('<Button-1>', make_on_click(hex_val))
            icon_label.bind('<Button-1>', make_on_click(hex_val))
            text_label.bind('<Button-1>', make_on_click(hex_val))

            def on_enter(frame):
                return lambda e: frame.config(bg='#e0e8f0')
            def on_leave(frame):
                return lambda e: frame.config(bg='#f0f0f0')

            btn_frame.bind('<Enter>', on_enter(btn_frame))
            btn_frame.bind('<Leave>', on_leave(btn_frame))

            self.dye_buttons.append(btn_frame)
            self.all_buttons.append(btn_frame)

        for i in range(4):
            self.quick_frame.grid_columnconfigure(i, weight=1)
        for i in range(4):
            self.quick_frame.grid_rowconfigure(i, weight=1)

        self.export_btn = ttk.Button(self.right_content, text=self.lang["export"], command=self.save_result, width=20)
        self.export_btn.pack(pady=5)
        self.all_buttons.append(self.export_btn)

        self.update_sequence_display()
        self.update_times_display()

    def create_widgets(self):
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        main_canvas = tk.Canvas(main_container, highlightthickness=0)
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        main_scrollbar = ttk.Scrollbar(main_container, orient=tk.VERTICAL, command=main_canvas.yview)
        main_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        main_canvas.configure(yscrollcommand=main_scrollbar.set)

        main_frame = ttk.Frame(main_canvas)
        canvas_window = main_canvas.create_window((0, 0), window=main_frame, anchor=tk.NW)

        def on_frame_configure(event):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))

        def on_canvas_configure(event):
            main_canvas.itemconfig(canvas_window, width=event.width)

        main_frame.bind("<Configure>", on_frame_configure)
        main_canvas.bind("<Configure>", on_canvas_configure)

        def on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        main_canvas.bind_all("<MouseWheel>", on_mousewheel)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.result_canvas = tk.Canvas(left_frame, bg='#f0f0f0', width=450, height=450)
        self.result_canvas.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        self.lang_notebook = ttk.Notebook(right_frame)
        self.lang_notebook.pack(fill=tk.BOTH, expand=True)

        lang_tabs = {
            "简体中文": "zh_CN",
            "繁體中文": "zh_TW",
            "日本語": "ja_JP",
            "English": "en_US"
        }

        self.lang_tab_frames = {}
        for display_name, code in lang_tabs.items():
            tab_frame = ttk.Frame(self.lang_notebook)
            self.lang_notebook.add(tab_frame, text=display_name)
            self.lang_tab_frames[code] = tab_frame

        def on_tab_changed(event):
            selected = self.lang_notebook.index(self.lang_notebook.select())
            lang_codes = list(lang_tabs.values())
            if selected < len(lang_codes):
                self.change_language(lang_codes[selected])

        self.lang_notebook.bind('<<NotebookTabChanged>>', on_tab_changed)

        current_tab_index = list(lang_tabs.values()).index(self.current_lang)
        self.lang_notebook.select(current_tab_index)

        self.right_content = self.lang_tab_frames[self.current_lang]
        self.rebuild_content()

        status_bar_frame = ttk.Frame(self.root)
        status_bar_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=(0, 10))

        ttk.Separator(status_bar_frame, orient='horizontal').pack(fill=tk.X, pady=5)

        self.status_var = tk.StringVar(value=self.lang["idle"])
        self.status_label2 = ttk.Label(status_bar_frame, textvariable=self.status_var,
                                 font=("Arial", 9), foreground="gray")
        self.status_label2.pack(side=tk.LEFT, padx=5)

    def update_all_texts(self):
        current_status = self.status_var.get()
        if current_status in [LANGUAGES[code]["idle"] for code in LANGUAGES]:
            self.status_var.set(self.lang["idle"])
        elif "图片已保存在" in current_status or "Image saved at" in current_status:
            pass

        self.status_label.config(text=self.lang["current_status"])
        self.version_label.config(text=self.lang["version"])
        self.version_title_label.config(text=self.lang["version"])
        self.armor_label.config(text=self.lang["armor_type"])
        self.armor_title_label.config(text=self.lang["armor_type"])
        self.body_label.config(text=self.lang["body_type"])
        self.body_title_label.config(text=self.lang["body_type"])
        self.color_display_label.config(text=self.lang["current_blend"])
        self.target_prefix_label.config(text=self.lang["target_color"])
        self.delta_prefix_label.config(text=self.lang["delta_e"])
        self.placeholder_label.config(text=self.lang["no_dye"])
        self.sequence_frame.config(text=self.lang["sequence"])
        self.clear_btn.config(text=self.lang["clear"])
        self.times_frame.config(text=self.lang["dye_times"])
        self.quick_frame.config(text=self.lang["dye_options"])
        self.export_btn.config(text=self.lang["export"])
        self.auto_gen_btn.config(text=self.lang["calc_sequence"])
        self.based_on_label.config(text=self.lang["based_on"])
        if hasattr(self, 'new_batch_btn') and self.new_batch_btn:
            self.new_batch_btn.config(text=self.lang["new_batch"])
        if hasattr(self, 'batch_render_btn') and self.batch_render_btn:
            self.batch_render_btn.config(text=self.lang["batch_render"])

        if self.armor_type == "horse_armor":
            armor_display_name = self.lang["horse_armor"]
            self.armor_display.config(text=armor_display_name, foreground="orange")
            body_display_name = "N/A"
            self.body_display.config(text=body_display_name, foreground="gray")
        elif self.armor_type == "wolf_armor":
            armor_display_name = self.lang["wolf_armor"]
            self.armor_display.config(text=armor_display_name, foreground="#C67B30")
            body_display_name = "N/A"
            self.body_display.config(text=body_display_name, foreground="gray")
            if hasattr(self, 'damage_display'):
                damage_display_name = {
                    "intact": self.lang["intact"],
                    "slightly_damaged": self.lang["slightly_damaged"],
                    "moderately_damaged": self.lang["moderately_damaged"],
                    "very_damaged": self.lang["very_damaged"]
                }.get(self.damage_level, self.damage_level)
                self.damage_display.config(text=damage_display_name)
        else:
            armor_display_name = {
                "helmet": self.lang["helmet"],
                "chestplate": self.lang["chestplate"],
                "leggings": self.lang["leggings"],
                "boots": self.lang["boots"]
            }.get(self.armor_type, self.armor_type)
            self.armor_display.config(text=armor_display_name, foreground="green")
            body_display_name = {
                "adult": self.lang["adult"],
                "baby": self.lang["baby"]
            }.get(self.body_type, self.body_type)
            self.body_display.config(text=body_display_name, foreground="purple")

        self.update_dye_button_texts()
        self.update_times_display()

    def update_dye_button_texts(self):
        for i, btn_frame in enumerate(self.dye_buttons):
            if i < len(self.color_data):
                hex_val, chinese_name, english_name = self.color_data[i]
                display_name = self.get_display_color_name(english_name)
                children = btn_frame.winfo_children()
                if len(children) >= 2:
                    text_label = children[1]
                    if isinstance(text_label, tk.Label):
                        text_label.config(text=display_name)

    def update_times_display(self):
        for english_name, label in self.times_labels.items():
            count = self.color_times.get(english_name, 0)
            display_name = self.get_display_color_name(english_name)
            label.config(text=f"{display_name}:{count}")
        self.root.update_idletasks()

    def on_canvas_configure(self, event):
        self.list_canvas.itemconfig(self.list_canvas_window, width=event.width)

    def on_inner_configure(self, event):
        self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))

    def select_version(self, version):
        if version == self.game_version:
            return

        old_batches = copy.deepcopy(self.batches)
        old_times = self.color_times.copy()

        self.game_version = version
        self.version_display.config(text=version)

        if self.armor_type == "horse_armor" or self.armor_type == "wolf_armor":
            self.image_size = self.get_image_size()
            self.load_armor_images()

        if version == "BE":
            self.max_batch_size = 20
            all_colors = self.get_all_colors()
            self.batches = [all_colors[:20]]
            if hasattr(self, 'new_batch_btn') and self.new_batch_btn:
                self.new_batch_btn.pack_forget()
        else:
            self.max_batch_size = None
            all_colors = self.get_all_colors()
            if all_colors:
                self.batches = []
                for i in range(0, len(all_colors), 9):
                    self.batches.append(all_colors[i:i+9])
            else:
                self.batches = [[]]
            if hasattr(self, 'new_batch_btn') and self.new_batch_btn:
                self.new_batch_btn.pack(side=tk.RIGHT, padx=5)

        self.current_batch_index = len(self.batches) - 1 if self.batches else 0

        for key in self.color_times:
            self.color_times[key] = 0
        for color in self.get_all_colors():
            english_name = self.get_english_name(color)
            if english_name and english_name in self.color_times:
                self.color_times[english_name] += 1

        self.update_sequence_display()
        self.update_times_display()
        self.update_display()

        self.set_status(self.lang["version_switched"].format(version), auto_reset=True)

    def select_body_type(self, body_type):
        if body_type == self.body_type:
            return

        self.body_type = body_type
        body_display_name = {
            "adult": self.lang["adult"],
            "baby": self.lang["baby"]
        }.get(body_type, body_type)
        self.body_display.config(text=body_display_name)

        self.image_size = self.get_image_size()
        self.load_armor_images()
        self.update_display()

        self.set_status(self.lang["body_switched"].format(body_display_name), auto_reset=True)

    def select_damage_level(self, damage_level):
        if damage_level == self.damage_level:
            return

        self.damage_level = damage_level
        damage_display_name = {
            "intact": self.lang["intact"],
            "slightly_damaged": self.lang["slightly_damaged"],
            "moderately_damaged": self.lang["moderately_damaged"],
            "very_damaged": self.lang["very_damaged"]
        }.get(damage_level, damage_level)
        
        if hasattr(self, 'damage_display'):
            self.damage_display.config(text=damage_display_name)

        self.load_armor_images()
        self.update_display()

        self.set_status(self.lang["damage_switched"].format(damage_display_name), auto_reset=True)

    def select_armor_type(self, armor_type):
        if armor_type == self.armor_type:
            return

        self.armor_type = armor_type
        armor_display_name = {
            "helmet": self.lang["helmet"],
            "chestplate": self.lang["chestplate"],
            "leggings": self.lang["leggings"],
            "boots": self.lang["boots"],
            "horse_armor": self.lang["horse_armor"],
            "wolf_armor": self.lang["wolf_armor"]
        }.get(armor_type, armor_type)
        self.armor_display.config(text=armor_display_name)

        if armor_type == "horse_armor" or armor_type == "wolf_armor":
            for btn in self.body_btns:
                btn.config(state='disabled')
            self.body_display.config(text="N/A", foreground="gray")
            if armor_type == "wolf_armor":
                for btn in self.damage_btns:
                    btn.config(state='normal')
                if hasattr(self, 'damage_label'):
                    self.damage_label.pack(side=tk.LEFT, padx=5)
                    self.damage_display.pack(side=tk.LEFT, padx=5)
            else:
                for btn in self.damage_btns:
                    btn.config(state='disabled')
                if hasattr(self, 'damage_label'):
                    self.damage_label.pack_forget()
                    self.damage_display.pack_forget()
        else:
            for btn in self.body_btns:
                btn.config(state='normal')
            body_display_name = {
                "adult": self.lang["adult"],
                "baby": self.lang["baby"]
            }.get(self.body_type, self.body_type)
            self.body_display.config(text=body_display_name, foreground="purple")
            for btn in self.damage_btns:
                btn.config(state='disabled')
            if hasattr(self, 'damage_label'):
                self.damage_label.pack_forget()
                self.damage_display.pack_forget()

        self.image_size = self.get_image_size()
        self.load_armor_images()
        self.update_display()

        self.set_status(self.lang["armor_switched"].format(armor_display_name), auto_reset=True)

    def add_new_batch(self):
        if self.game_version == "BE":
            self.set_status(self.lang["be_mode_no_batch"], auto_reset=True)
            return

        self.batches.append([])
        self.current_batch_index = len(self.batches) - 1
        self.update_sequence_display()
        self.update_batch_count()
        self.set_status(self.lang["batch_created"].format(len(self.batches), len(self.batches)), auto_reset=True)

    def set_current_batch(self, batch_idx):
        if 0 <= batch_idx < len(self.batches):
            self.current_batch_index = batch_idx

            for key in self.color_times:
                self.color_times[key] = 0
            for batch in self.batches:
                for color in batch:
                    english_name = self.get_english_name(color)
                    if english_name and english_name in self.color_times:
                        self.color_times[english_name] += 1

            self.update_sequence_display()
            self.update_batch_count()
            self.update_times_display()
            self.update_display()
            self.set_status(self.lang["switch_batch"].format(batch_idx + 1), auto_reset=True)

    def update_batch_count(self):
        self.batch_count_label.config(text=f"{self.lang['batch']}: {len(self.batches)}")

    def add_color_to_sequence(self, hex_val):
        english_name = self.get_english_name(hex_val)

        if not self.batches:
            self.batches.append([])
            self.current_batch_index = 0

        current_batch = self.batches[self.current_batch_index]

        if self.game_version == "BE" and len(current_batch) >= self.max_batch_size:
            self.set_status(self.lang["be_max_length"], auto_reset=True)
            return False

        if self.game_version == "JE" and len(current_batch) >= 9:
            self.set_status(self.lang["batch_full_hint"], auto_reset=True)
            return False

        old_color = self.calculate_blend_color()

        current_batch.append(hex_val)

        new_color = self.calculate_blend_color()

        if new_color != old_color:
            if english_name and english_name in self.color_times:
                self.color_times[english_name] += 1
                self.update_times_display()
            self.update_sequence_display()
            self.update_display()
            return True
        else:
            current_batch.pop()
            display_name = self.get_display_color_name(english_name) if english_name else hex_val
            self.set_status(self.lang["invalid_add"].format(display_name), auto_reset=True)
            return False

    def remove_color_from_batch(self, batch_idx, color_idx):
        if batch_idx < len(self.batches) and color_idx < len(self.batches[batch_idx]):
            del self.batches[batch_idx][color_idx]

            for key in self.color_times:
                self.color_times[key] = 0
            for batch in self.batches:
                for color in batch:
                    english_name = self.get_english_name(color)
                    if english_name and english_name in self.color_times:
                        self.color_times[english_name] += 1

            if not self.batches[batch_idx] and len(self.batches) > 1:
                del self.batches[batch_idx]
                if self.current_batch_index >= len(self.batches):
                    self.current_batch_index = len(self.batches) - 1
                self.update_batch_count()

            self.update_times_display()
            self.update_sequence_display()
            self.update_display()

    def clear_batch(self, batch_idx):
        if batch_idx < len(self.batches):
            self.batches[batch_idx] = []
            if not self.batches[batch_idx] and len(self.batches) > 1:
                del self.batches[batch_idx]
                if self.current_batch_index >= len(self.batches):
                    self.current_batch_index = len(self.batches) - 1
                elif batch_idx == self.current_batch_index:
                    self.current_batch_index = len(self.batches) - 1
                self.update_batch_count()

            for key in self.color_times:
                self.color_times[key] = 0
            for batch in self.batches:
                for color in batch:
                    english_name = self.get_english_name(color)
                    if english_name and english_name in self.color_times:
                        self.color_times[english_name] += 1

            self.update_times_display()
            self.update_sequence_display()
            self.update_display()

    def clear_sequence(self):
        self.batches = [[]]
        self.current_batch_index = 0
        for key in self.color_times:
            self.color_times[key] = 0
        self.use_target = False
        self.target_color = (255, 255, 255)
        self.target_hex = "#FFFFFF"
        self.update_batch_count()
        self.update_times_display()
        self.update_sequence_display()
        self.update_display()
        self.set_status(self.lang["idle"])

    def delete_batch(self, batch_idx):
        if 0 <= batch_idx < len(self.batches):
            if len(self.batches) == 1:
                self.batches[0] = []
                self.current_batch_index = 0
            else:
                del self.batches[batch_idx]
                if not self.batches:
                    self.batches = [[]]
                    self.current_batch_index = 0
                elif self.current_batch_index >= len(self.batches):
                    self.current_batch_index = len(self.batches) - 1
                elif batch_idx == self.current_batch_index:
                    self.current_batch_index = len(self.batches) - 1
                elif batch_idx < self.current_batch_index:
                    self.current_batch_index -= 1

            for key in self.color_times:
                self.color_times[key] = 0
            for batch in self.batches:
                for color in batch:
                    english_name = self.get_english_name(color)
                    if english_name and english_name in self.color_times:
                        self.color_times[english_name] += 1

            self.update_batch_count()
            self.update_times_display()
            self.update_sequence_display()
            self.update_display()

    def update_sequence_display(self):
        for item in self.list_items:
            item.destroy()
        for label in self.batch_labels:
            label.destroy()
        self.list_items.clear()
        self.batch_labels.clear()

        for batch_idx, batch in enumerate(self.batches):
            is_current = (batch_idx == self.current_batch_index)
            bg_color = '#d4e8ff' if is_current else '#e8e8e8'

            if self.game_version == "BE":
                batch_label = tk.Label(self.list_inner,
                                       text=f"{self.lang['sequence_self']}（{len(batch)}/{self.max_batch_size}）",
                                       bg=bg_color, font=("Arial", 9, "bold"))
            else:
                batch_label = tk.Label(self.list_inner,
                                       text=f"{self.lang['batch_prefix']}{batch_idx + 1}（{len(batch)}/9）",
                                       bg=bg_color, font=("Arial", 9, "bold"), cursor="hand2")
                batch_label.bind('<Button-1>', lambda e, bi=batch_idx: self.set_current_batch(bi))
            batch_label.pack(fill=tk.X, pady=(5, 2))
            self.batch_labels.append(batch_label)

            if not batch:
                empty_label = tk.Label(self.list_inner, text=f"  {self.lang['batch_empty']}",
                                       bg='white', font=("Arial", 8), fg='gray')
                empty_label.pack(fill=tk.X, pady=1)
                self.list_items.append(empty_label)
            else:
                for color_idx, color in enumerate(batch):
                    item_frame = tk.Frame(self.list_inner, bg='white', height=24)
                    item_frame.pack(fill=tk.X, pady=1)

                    r, g, b = self.hex_to_rgb(color)
                    color_hex = f'#{r:02x}{g:02x}{b:02x}'
                    square = tk.Canvas(item_frame, width=14, height=14, bg=color_hex,
                                       highlightthickness=1, highlightcolor='gray')
                    square.pack(side=tk.LEFT, padx=(5, 6))

                    color_name = self.get_color_name_by_hex(color)
                    label = tk.Label(item_frame, text=f"{color_idx+1}. {color_name}",
                                     bg='white', font=("Arial", 9))
                    label.pack(side=tk.LEFT)

                    del_btn = tk.Label(item_frame, text="×", fg='red', bg='white',
                                       font=("Arial", 11, "bold"), cursor="hand2")
                    del_btn.pack(side=tk.RIGHT, padx=8)
                    del_btn.bind('<Button-1>',
                                 lambda e, bi=batch_idx, ci=color_idx: self.remove_color_from_batch(bi, ci))

                    self.list_items.append(item_frame)

            if self.game_version == "JE":
                control_frame = tk.Frame(self.list_inner, bg='#f8f8f8')
                control_frame.pack(fill=tk.X, pady=(2, 5))

                clear_batch_btn = tk.Label(control_frame, text=self.lang["clear_batch"],
                                           fg='blue', bg='#f8f8f8', font=("Arial", 8), cursor="hand2")
                clear_batch_btn.pack(side=tk.LEFT, padx=10)
                clear_batch_btn.bind('<Button-1>', lambda e, bi=batch_idx: self.clear_batch(bi))

                if len(self.batches) > 1:
                    del_batch_btn = tk.Label(control_frame, text=self.lang["delete_batch"],
                                             fg='red', bg='#f8f8f8', font=("Arial", 8), cursor="hand2")
                    del_batch_btn.pack(side=tk.LEFT, padx=5)
                    del_batch_btn.bind('<Button-1>', lambda e, bi=batch_idx: self.delete_batch(bi))

                self.list_items.append(control_frame)

        self.update_batch_count()
        self.update_color_display()

        self.list_canvas.update_idletasks()
        self.list_canvas.configure(scrollregion=self.list_canvas.bbox("all"))

    def select_list_item(self, index):
        pass

    def remove_item(self, index):
        pass

    def update_dye_buttons(self):
        for i, (hex_val, chinese_name, english_name) in enumerate(self.color_data):
            img = self.dye_images.get(hex_val)
            if i < len(self.dye_icon_labels):
                icon_label = self.dye_icon_labels[i]
                if img:
                    icon_label.config(image=img)
                    icon_label.config(text='')
                else:
                    icon_label.config(text='■', font=('Arial', 10))

    def update_color_display(self):
        for widget in self.color_display_frame.winfo_children():
            if widget not in [self.batch_count_label]:
                widget.pack_forget()

        all_colors = self.get_all_colors()
        if not all_colors:
            self.placeholder_label.pack(side=tk.LEFT, padx=5)
            self.batch_count_label.pack(side=tk.RIGHT, padx=5)
            return

        self.color_display_label.pack(side=tk.LEFT, padx=3)
        self.current_color_preview.pack(side=tk.LEFT, padx=3)
        self.current_color_label.pack(side=tk.LEFT, padx=3)

        self.target_prefix_label.pack(side=tk.LEFT, padx=(5, 3))
        self.target_color_preview.pack(side=tk.LEFT, padx=3)
        self.target_color_label.pack(side=tk.LEFT, padx=3)

        self.delta_prefix_label.pack(side=tk.LEFT, padx=(5, 3))
        self.delta_e_label.pack(side=tk.LEFT, padx=3)

        current_rgb = self.calculate_blend_color()
        self.current_blend_color = current_rgb
        current_hex = self.rgb_to_hex(current_rgb[0], current_rgb[1], current_rgb[2])
        self.current_color_preview.config(bg=current_hex)
        self.current_color_label.config(text=current_hex)

        if self.use_target:
            target_rgb = self.target_color
            self.target_color_preview.config(bg=self.target_hex)
            self.target_color_label.config(text=self.target_hex)
        else:
            target_rgb = current_rgb
            self.target_color = current_rgb
            self.target_hex = current_hex
            self.target_color_preview.config(bg=current_hex)
            self.target_color_label.config(text=current_hex)

        delta_e = self.calculate_delta_e(current_rgb, target_rgb)
        self.delta_e_label.config(text=f"{delta_e:.2f}")
        if delta_e < 1.0:
            self.delta_e_label.config(foreground="green")
        elif delta_e < 3.0:
            self.delta_e_label.config(foreground="orange")
        else:
            self.delta_e_label.config(foreground="red")

        self.batch_count_label.pack(side=tk.RIGHT, padx=5)

    def hex_to_rgb(self, hex_str):
        hex_str = hex_str.strip()
        if not hex_str.startswith('#'):
            hex_str = '#' + hex_str
        try:
            if len(hex_str) == 7:
                r = int(hex_str[1:3], 16)
                g = int(hex_str[3:5], 16)
                b = int(hex_str[5:7], 16)
                return r, g, b
            elif len(hex_str) == 4:
                r = int(hex_str[1]*2, 16)
                g = int(hex_str[2]*2, 16)
                b = int(hex_str[3]*2, 16)
                return r, g, b
            else:
                return 255, 255, 255
        except:
            return 255, 255, 255

    def rgb_to_hex(self, r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'.upper()

    def update_display(self):
        try:
            if not self.images:
                return

            final_img = self.render_single_image()

            canvas_width = self.result_canvas.winfo_width()
            canvas_height = self.result_canvas.winfo_height()

            if canvas_width <= 1:
                canvas_width = 450
                canvas_height = 450

            img_width, img_height = final_img.size
            ratio = min(canvas_width/img_width, canvas_height/img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            preview_resized = final_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            result_tk = ImageTk.PhotoImage(preview_resized)
            self.result_canvas.delete("all")
            self.result_canvas.create_image(canvas_width//2, canvas_height//2,
                                            image=result_tk, anchor=tk.CENTER)
            self.result_canvas.image = result_tk

        except Exception as e:
            print(self.lang["render_error"].format(e))

    def save_result(self):
        try:
            if not self.images:
                self.set_status(self.lang["error_no_image"], auto_reset=True)
                return

            final_img = self.render_single_image()

            filename = self.generate_filename() + ".png"
            file_path = os.path.join(self.output_dir, filename)

            final_img.save(file_path, 'PNG')
            self.set_status(self.lang["image_saved"].format(file_path), auto_reset=True)

        except Exception as e:
            self.set_status(self.lang["error"].format(str(e)), auto_reset=True)


def main():
    root = tk.Tk()
    app = ImageBlendApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
