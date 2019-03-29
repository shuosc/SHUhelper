FROM node:11.9.0-alpine
COPY ./frontend/ ./
RUN apk add git && npm install nuxt -g && npm install --production
ENV HOST 0.0.0.0
ENV PORT 80
ENV NODE_ENV production
EXPOSE 80
CMD ["npm","run","start"]
