# 3ES

This template should help get you started developing with Vue 3 in Vite.

## Lokale SSL-Zertifikate installieren
Diese werden gebraucht, da ansonsten auf dem Iphone der Kamera-Feed nicht funktioniert.

1. mkcert installieren (Mac: brew install mkcert, Windows: choco install mkcert) [tutorial](https://github.com/FiloSottile/mkcert)

2. mkcert -install

Danach ist ein lokales Zertifikat installiert
Um das Zertifikat auch auf dem Iphone zu haben, kann man es einfach Air-dropen und installieren.
Das Zertifikat befindet sich bei dem Pfad, welcher "mkcert -CAROOT" zurückgibt


## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```
The Dev-Server is also in your locale Network accessible

### Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```

### Run End-to-End Tests with [Cypress](https://www.cypress.io/)

```sh
npm run test:e2e:dev
```

This runs the end-to-end tests against the Vite development server.
It is much faster than the production build.

But it's still recommended to test the production build with `test:e2e` before deploying (e.g. in CI environments):

```sh
npm run build
npm run test:e2e
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```
