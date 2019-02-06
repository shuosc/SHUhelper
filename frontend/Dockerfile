FROM node:11.6.0-alpine
COPY ./frontend/ ./
RUN npm install nuxt -g && npm install --production
ENV HOST 0.0.0.0
ENV PORT 80
ENV NODE_ENV production
EXPOSE 80
CMD ["npm","run","start"]