export DEBUGGING=1
export PORT=3000
export DB_HOST=172.19.0.2
export DB_NAME=octopus
export DB_PORT=3306
export DB_USER=root
export DB_PASS=root
export REDIS_HOST='redis://172.19.0.3:6379'
export SALT='it is salty'
export PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQDeUQU6jLD8Ez+om48UWaBpLFuJR24iD4m/BhVALmGeQkp+eRCk
25dQsrJSDJ7hjerrdj0ZfxGuDgnmVmOcqtIvQR79GxSYn4OYcP7gMCSk9R13OAx3
CwfpAaHISd6/DsIxAiJ8INOA3qqWsEfKp6RnTmTXQi35IRdTrrsHrAiziwIDAQAB
AoGADUb1cvu4DjXwFVfFAcgghmd5yAcWEr6u0VPBrSWX+uWmoUsFrXLX5J/nenL6
gioBn7JeD8nA+o4oFTOPm2mwR7mma6lrx/cm+Ulz2JrMvoU1F+juTtAoTiYFmi19
i7Xxdvrxis3IEOhpNSeqN7Q894rSsuiQD58WpMR4hTWyjlECQQDg7bEeeLlSGmF1
jVqw/YVDS2hwtP5Y6Cr1h1vqc7UX4IrrcJxce1Qx/8X+/S/6H0B4CwK0KH9o/Nbx
erAmHKdNAkEA/Qb1ZjYCbg18i+rH6DziFclZ3QrVBNrqPZEOo7hmvmykXIO2vHBU
aQeW8nohYoVMAHTtEKO/Gvr4i7hRXFbKNwJBAMYrJH2AR2Y6r9rtqxV8h0h+y4lh
LSYPhqnDlAu/3bEnt70u/dPNJKTYgAzj7L0lg5s/uCYZ+Ab7nDQsr70kSZECQQC0
d30Z7JWpFtdpGAiC/MGoFleQz4QFlXoSdV6CqSgm02gbUBpKpredvbsMsM0U7su5
W6wl/RR10uDpDoqBGKnbAkEAzNNQTrPv6cnSMko9ccjyyq70i5myxMyuJdLsLKMH
xNO09nMsdTVxfGJBgvAN8zSFsHOPyLqFWJVJlAOZCpz/aw==
-----END RSA PRIVATE KEY-----"

celery -A run_celery.CELERY worker --loglevel=info