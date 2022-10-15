# Sosanie Ebla Bot Premium™

> *алёна (флирт) снова в деле, сучки!*

## What in the World Is This?

Combining the power of premium text-to-speech models from the likes of [Yandex](https://cloud.yandex.ru/services/speechkit) and [Tinkoff](https://voicekit.tinkoff.ru/) with the power of [Telegram](https://telegram.org/), this bot allows you to send voice messages to your friends and family with the voice of your choice.

### But Why?

It's fun. \
Unfortunatelly, it is not practical.

## How to Use

### Warnings / Precautions

#### Regarding the Code

It's probably not the prettiest code you've ever seen. \
It's probably not the most efficient code you've ever seen. \
It's probably not the most secure code you've ever seen. \
It's probably not the most well-documented code you've ever seen. \
It probably has not the prettiest logging you've ever seen.

#### Regarding the API

##### Tinkoff

##### Yandex

### Host Yourself

#### Docker

With the provided `Dockerfile`s and `docker-compose.yml` (or prebuilt `amd64` as specified in `docker-compose.yml`), you can easily deploy the bot.

1. Clone the repository.
2. `docker-compose up -d` with all the necessary environment variables set (see below).
3. Enjoy!

### Use the Official Bot

## Internal Structure

### Environment Variables

| Variable | Description |
| -------- | ----------- |
| `DB_MONGODB_USERNAME` | MongoDB username |
| `DB_MONGODB_PASSWORD` | MongoDB username |
| `DB_MONGODB_DATABASE` | Default initializable databse  |
| `DB_PATH_VOLUME` | Host path for database persistent files |
| `TINKOFF_VOICEKIT_APIKEY` | API key generated in VoiceKit console |
| `TINKOFF_VOICEKIT_SECRETKEY` | API secret key generated in VoiceKit console |
| `TINKOFF_VOICEKIT_ENDPOINTAPI` | Tinkoff's AI API endpoint |
| `YANDEX_SPEECHKIT_FOLDERID` | Yandex.Cloud account folder ID |
| `YANDEX_SPEECHKIT_APITOKEN` | Generated static main API token for a given Yandex.Cloud account |
| `VPRW_API_KEY` | API key used for bot authentication and API communication |
| `VPRW_API_ENDPOINT` | Endpoint value (FQDN) |
| `API_CONTACT_EMAIL` | Contact e-mail displayed in the docs |
| `DB_MONGODB_URI` | MongoDB URI for authentication |
| `VOICEMESSAGES_PATH_VOLUME` | Host path for voice-messages storage |
| `TELEGRAM_API_ID` | Telegram API ID generated in the Telegram.API console |
| `TELEGRAM_API_HASH` | Telegram API hash generated in the Telegram.API console |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token |
| `BOT_CONTACT_USERNAME` | Contact username displayed in the contact information |

### Bot

### API

### Database
