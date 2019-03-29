FROM node:11.6.0-alpine
COPY ./backend ./backend
COPY ./shared ./shared
RUN cd ./backend && npm install --production && cd ../shared && npm install --production && cd ..
WORKDIR ./backend
EXPOSE 3001
ENV NODE_ENV development
CMD ["node","./src/main.js"]
