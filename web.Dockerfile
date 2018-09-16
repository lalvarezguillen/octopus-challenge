FROM node as frontend-build
WORKDIR /home/app
COPY frontend ./frontend
COPY package.json .
COPY webpack.config.js .
RUN npm i && npm run build


FROM python
WORKDIR /home/app
COPY --from=frontend-build /home/app/dist ./dist 
COPY backend ./backend
COPY run_app.py .
COPY requirements.dist.txt .
RUN pip install -r requirements.dist.txt