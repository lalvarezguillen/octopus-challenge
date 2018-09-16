FROM node as frontend-build
WORKDIR /home/app
COPY frontend ./frontend
COPY package.json .
COPY webpack.config.js .
RUN npm i && npm run build


FROM python:3.6
EXPOSE 80
WORKDIR /home/app
COPY --from=frontend-build /home/app/dist ./dist 
COPY backend ./backend
COPY run_app.py .
COPY requirements.dist.txt .
RUN pip install -r requirements.dist.txt
CMD ["python", "run_app.py"]