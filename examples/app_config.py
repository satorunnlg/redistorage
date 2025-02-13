from redistorage.model import RedisStorageModel

class AppConfig(RedisStorageModel):
    """ アプリケーション設定モデル """
    
    system_name = "My Web App"
    enable_feature_x = True
    max_connections = 100
    theme = "dark"

    class Meta:
        redis_key = "app_config"
        verbose_name = "アプリケーション設定"

# 使い方
config = AppConfig()
print(config.system_name)  # "My Web App"
config.theme = "light"
config.save()  # 変更を保存
