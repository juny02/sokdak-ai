# sokdak-ai

FastAPI 기반 대화 생성 서버입니다.

페르소나를 설정해 대화할 수 있습니다.


## 🚀 Run with Docker

아래 명령어로 실행합니다.

**For Production**

```bash
docker  compose  up  --build
```

**For Development**
```bash
docker compose -f compose.dev.yml --env-file .env.dev up --build
```

## 🧪 How to Test
아래 명령어로 전체 테스트를 실행할 수 있습니다.

```bash
uv run pytest .
```