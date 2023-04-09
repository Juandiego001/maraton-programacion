// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    telemetry: false,
    app: {
        head: {
            link: [
                {
                    rel: "stylesheet",
                    href: "/css/global.css"
                }
            ]
        }
    }
})
