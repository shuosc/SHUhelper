FROM node:11.6.0-alpine
COPY ./frontend/.nuxt ./.nuxt
COPY ./frontend/modules ./modules
COPY ./frontend/nuxt.config.js ./nuxt.config.js
COPY ./frontend/package.json ./package.json
RUN npm install nuxt -g && npm install --production
ENV HOST 0.0.0.0
ENV PORT 80
ENV NODE_ENV production
EXPOSE 80
CMD ["npm","run","start"]