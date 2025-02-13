import json
import redis
import threading
import time

REDIS_LOCK_TIMEOUT = 5  # ロックの有効期限（秒）

class RedisStorageModel:
    """ Redis をストレージとして使用するデータモデル（スレッドセーフ & マルチプロセス対応） """

    _lock = threading.Lock()  # スレッドロック（クラスレベルで管理）

    def __init__(self):
        """ インスタンス生成時に Redis から最新のデータをロード """
        self.redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
        self.REDIS_KEY = f"redistorage_{getattr(self.Meta, 'redis_key', self.__class__.__name__)}"
        self.REDIS_LOCK_KEY = f"{self.REDIS_KEY}_lock"  # ロック用のキー

        self._load_data()  # データのロード

    def _load_data(self):
        """ Redis からデータをロードし、なければデフォルト値をセット """
        with self._lock:
            data = self.redis_client.get(self.REDIS_KEY)
            self.data = json.loads(data) if data else self._get_defaults()
            for key, default in self._get_defaults().items():
                if key not in self.data:
                    self.data[key] = default
            self._apply_data()

    def _apply_data(self):
        """ クラス変数としてデータを適用 """
        for key, value in self.data.items():
            if key in self._get_defaults():
                setattr(self, key, value)

    def _get_defaults(self):
        """ クラス変数からデフォルト値を取得 """
        return {key: value for key, value in self.__class__.__dict__.items() if not key.startswith("__") and not callable(value)}

    def _acquire_lock(self):
        """ Redis のロックを取得 """
        start_time = time.time()
        while time.time() - start_time < REDIS_LOCK_TIMEOUT:
            if self.redis_client.setnx(self.REDIS_LOCK_KEY, 1):
                self.redis_client.expire(self.REDIS_LOCK_KEY, REDIS_LOCK_TIMEOUT)
                return True
            time.sleep(0.1)
        return False

    def _release_lock(self):
        """ Redis のロックを解除 """
        self.redis_client.delete(self.REDIS_LOCK_KEY)

    def save(self):
        """ データを保存（スレッド & マルチプロセスセーフ） """
        with self._lock:
            if not self._acquire_lock():
                raise TimeoutError("別のプロセスがデータを保存中です。")

            try:
                new_data = {key: getattr(self, key) for key in self._get_defaults()}
                self.redis_client.set(self.REDIS_KEY, json.dumps(new_data))
                self.data = new_data
            finally:
                self._release_lock()

    def reload(self):
        """ データをリロード """
        self._load_data()

    class Meta:
        redis_key = "default_storage_model"
        verbose_name = "汎用 Redis ストレージモデル"
