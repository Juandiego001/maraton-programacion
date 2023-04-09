<template>
    <div class="container">
        <h2>MARATÓN DE PROGRAMACIÓN</h2>

        <form>
            <div>
                <div>
                    <label for="email">Ingresa tu correo</label>
                    <input class="" id="email" name="email" type="email" autocomplete="email" />
                </div>
                <div>
                    <label for="password">Ingresa tu contraseña</label>
                    <input class="" id="password" name="password" type="password" autocomplete="current-password" />
                </div>
                <div class="container-buttons">
                    <button>Iniciar sesión</button>
                    <button>Registrarse</button>
                </div>
            </div>
        </form>
    </div>
</template>

<script setup>

useHead({
    link: {
        rel: "stylesheet",
        href: "/css/index.css"
    }
})

</script>