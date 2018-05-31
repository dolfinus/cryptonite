FROM mhart/alpine-node:latest as node_build
WORKDIR /opt/cryptonite
COPY package.json .
RUN npm install
COPY src ./src
COPY webpack.config.js .
COPY jslintrc.json .
COPY .eslintrc.json .
COPY .babelrc .
RUN npm run build

FROM nginx:alpine
WORKDIR /opt/cryptonite
COPY --from=node_build /opt/cryptonite/dist ./dist
COPY index.html .
COPY cryptonite.nginx /etc/nginx/conf.d/default.conf
