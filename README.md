# Сборка
```
docker build -t wekan-telegram-bot .
```

# Запуск
```
docker run --env TELEGRAM_API_KEY="<TELEGRAM_API_KEY>" --env TELEGRAM_GROUP_CHAT_ID="<GROUP_CHAT_ID>" --env WEKAN_BASE_URL="<WEKAN_URL>" --env WEKAN_LOGIN="<WEKAN_LOGIN>" --env WEKAN_PASSWORD="<WEKAN_PASSWORD>" -d wekan-telegram-bot
```