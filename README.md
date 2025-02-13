# **redistorage - A Redis-based Persistent Model for Python**

[![PyPI](https://img.shields.io/pypi/v/redistorage)](https://pypi.org/project/redistorage/)
[![Python Version](https://img.shields.io/pypi/pyversions/redistorage)](https://pypi.org/project/redistorage/)
[![License](https://img.shields.io/pypi/l/redistorage)](https://github.com/yourusername/redistorage/blob/main/LICENSE)
[![Build](https://github.com/yourusername/redistorage/actions/workflows/pypi-publish.yml/badge.svg)](https://github.com/yourusername/redistorage/actions)

**redistorage** は、**Redis をストレージとして活用する Python モデルライブラリ** です。  
Django の `models.Model` のように、**シンプルな Python クラスとしてデータ管理** が可能で、設定管理・キャッシュ・セッション管理などに適しています。  

✅ **Redis に自動保存 & 取得**  
✅ **Django モデルのようなシンプルな操作**  
✅ **スレッド & マルチプロセスセーフ**  
✅ **設定・キャッシュ・セッション管理に最適**  
✅ **GitHub Actions を使った PyPI への自動デプロイ**

---

## **🔧 インストール**
PyPI から `pip` でインストールできます：
```bash
pip install redistorage
```

---

## **🚀 クイックスタート**
### **1️⃣ モデルを定義**
まず、`RedisStorageModel` を継承してクラスを作成します。

```python
from redistorage.model import RedisStorageModel

class AppConfig(RedisStorageModel):
    """ アプリケーション設定モデル """
    
    system_name = "My Web App"
    enable_feature_x = True
    max_connections = 100
    theme = "dark"

    class Meta:
        redis_key = "app_config"  # Redis に保存されるキー
        verbose_name = "アプリケーション設定"
```

---

### **2️⃣ インスタンス化してデータを取得**
インスタンス化すると、**Redis からデータが自動的にロード** されます。
```python
config = AppConfig()
print(config.system_name)  # "My Web App"
print(config.theme)        # "dark"
```

---

### **3️⃣ 値を変更**
データを変更し、`save()` で保存できます。
```python
config.theme = "light"  # インスタンス内で変更
config.save()  # Redis & JSON に反映（スレッドセーフ）
```

---

### **4️⃣ 他のプロセスで再取得**
保存されたデータは **Redis に永続化** されているため、別のプロセスでも同じ値を取得できます。
```python
new_config = AppConfig()
print(new_config.theme)  # "light"（変更が反映されている）
```

---

### **5️⃣ データをリロード**
変更を破棄し、Redis に保存されている値に戻したい場合：
```python
config.reload()  # Redis から最新の設定を取得
```

---

## **🔑 特徴**
### ✅ **1. シンプルで直感的な操作**
- Django の `models.Model` に似た API で、Python のクラス変数としてデータを定義
- `config.theme = "light"` のように **自然なデータ操作**
- `save()` で Redis & JSON に自動保存

### ✅ **2. スレッド & マルチプロセスセーフ**
- `threading.Lock()` + Redis の `SETNX` により、**データ競合を防止**
- **複数スレッド・複数プロセス** から同時に `save()` を実行しても安全

### ✅ **3. Redis をストレージとして活用**
- すべてのデータは **Redis に保存され、永続化**
- 別プロセス・別サーバーからでもデータにアクセス可能
- **設定管理・キャッシュ・セッション管理に最適**

### ✅ **4. GitHub Actions による PyPI 自動デプロイ**
- **GitHub にタグを push するだけ** で PyPI に自動デプロイ
- `pip install redistorage` でいつでも利用可能

---

## **🛠️ 高度な機能**
### **🔹 メタ情報の設定**
`Meta` クラスを使って **Redis のキー名** や **説明** を設定できます。
```python
class CustomConfig(RedisStorageModel):
    custom_value = 42

    class Meta:
        redis_key = "custom_config"
        verbose_name = "カスタム設定"
```

---

## **📝 ユニットテスト**
### **テストを実行**
`pytest` または `unittest` でテスト可能：
```bash
python -m unittest tests/test_model.py
```

### **`tests/test_model.py`**
```python
import unittest
from redistorage.model import RedisStorageModel

class TestRedisStorageModel(unittest.TestCase):

    class SampleConfig(RedisStorageModel):
        system_name = "Test System"
        debug = True

        class Meta:
            redis_key = "test_config"

    def test_initial_values(self):
        config = self.SampleConfig()
        self.assertEqual(config.system_name, "Test System")
        self.assertTrue(config.debug)

    def test_save_and_reload(self):
        config = self.SampleConfig()
        config.system_name = "Updated System"
        config.save()

        new_config = self.SampleConfig()
        self.assertEqual(new_config.system_name, "Updated System")

if __name__ == "__main__":
    unittest.main()
```

---

## **📦 開発 & デプロイ**
### **開発環境をセットアップ**
```bash
git clone https://github.com/yourusername/redistorage.git
cd redistorage
pip install -r requirements.txt
```

### **PyPI に手動デプロイ**
```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

### **GitHub Actions による PyPI 自動デプロイ**
- **`git tag v1.0.0 && git push origin v1.0.0`** で **PyPI に自動デプロイ！**

---

## **📜 ライセンス**
`redistorage` は **MIT License** のもとで公開されています。

---

## **🌍 リンク**
- **GitHub:** [https://github.com/yourusername/redistorage](https://github.com/yourusername/redistorage)
- **PyPI:** [https://pypi.org/project/redistorage/](https://pypi.org/project/redistorage/)
- **Issue & バグ報告:** [https://github.com/yourusername/redistorage/issues](https://github.com/yourusername/redistorage/issues)

---

## **🎯 まとめ**
✅ **Redis を使ったシンプルなデータ管理モデル**  
✅ **スレッド & マルチプロセス対応で安全**  
✅ **Django の `models.Model` に似た直感的な使い方**  
✅ **GitHub Actions で PyPI に自動デプロイ可能！**  

🚀 **`redistorage` を活用して、簡単に Redis を活用したデータ管理を始めましょう！** 🎉