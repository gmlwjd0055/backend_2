# GitHub Actions 배포 설정

운영 대상은 서로 다른 Windows 컴퓨터입니다. 프론트엔드는 `100.100.100.11`의 Nginx에서 제공하고, 백엔드는 `100.100.100.12:8000`에서 Uvicorn으로 실행합니다. 프론트엔드의 배포 API 주소는 `frontend/.env.production`에서 설정합니다.

현재 SSH 계정은 두 컴퓨터 모두 `test`입니다. 비밀번호는 저장소나 이 문서에 쓰지 말고 `DEPLOY_PASSWORD` GitHub Secret에 등록하세요. SSH 포트는 아직 확인되지 않았으므로 실제 포트를 확인해서 설정해야 합니다. 프론트엔드 Nginx 설치 경로는 `C:\Users\test\Downloads\nginx-1.30.5\nginx-1.30.5`이며, 백엔드 배포 폴더의 절대 경로는 아직 정해지지 않았습니다.

주의: 아래의 기존 워크플로 파일은 Linux 서버 경로/명령을 전제로 작성되어 있어 위 Windows 서버에 그대로 배포하면 안 됩니다. Windows OpenSSH의 원격 셸과 Nginx 문서 루트, 백엔드 폴더의 실제 절대 경로에 맞춘 워크플로 변경이 필요합니다.

## GitHub Secrets

저장소의 **Settings → Secrets and variables → Actions → New repository secret**에서 다음 값을 등록하세요.

| Secret 이름 | 값 |
| --- | --- |
| `DEPLOY_HOST` | 대상 Windows 컴퓨터 IP |
| `DEPLOY_SSH_PORT` | 해당 컴퓨터의 SSH 포트 |
| `DEPLOY_USER` | `test` |
| `DEPLOY_PASSWORD` | 계정 SSH 비밀번호 (저장소 파일에 기록 금지) |
| `DEPLOY_FINGERPRINT` | 해당 컴퓨터 SSH 호스트 키 SHA256 지문 |

SSH 호스트 지문은 신뢰할 수 있는 서버 콘솔에서 `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub`로 확인해 등록하세요. 워크플로는 지문을 확인해 SSH 서버를 검증합니다.

## 서버 준비

- Nginx는 `C:\Users\test\Downloads\nginx-1.30.5\nginx-1.30.5`에서 정적 빌드 결과물을 서비스합니다. Nginx 설정에서 실제 `root` 경로를 확인하세요.
- Uvicorn은 `100.100.100.12:8000`에서 실행하고, Windows 컴퓨터의 실제 `backend` 디렉터리를 확인하세요.
- 브라우저가 프론트엔드 도메인/IP에서 백엔드로 직접 요청하므로 백엔드 CORS에 Nginx 사이트의 origin을 허용해야 합니다.
