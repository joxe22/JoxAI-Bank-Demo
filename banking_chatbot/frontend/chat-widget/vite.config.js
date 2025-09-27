/**
 * ⚡ Configuración de Vite
 * Ubicación: frontend/chat-widget/vite.config.js
 */

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'

export default defineConfig({
    plugins: [react()],

    // Configuración del servidor de desarrollo
    server: {
        port: 3000,
        host: true,
        cors: true
    },

    // Configuración de build
    build: {
        outDir: 'dist',
        sourcemap: true,

        // Configuración para widget embebible
        lib: {
            entry: resolve(__dirname, 'src/main.jsx'),
            name: 'BankingChatWidget',
            fileName: (format) => `banking-chat-widget.${format}.js`
        },

        rollupOptions: {
            // Externalizar React si se va a usar como widget embebible
            external: process.env.NODE_ENV === 'production' ? [] : ['react', 'react-dom'],

            output: {
                globals: {
                    react: 'React',
                    'react-dom': 'ReactDOM'
                }
            }
        }
    },

    // Resolve aliases
    resolve: {
        alias: {
            '@': resolve(__dirname, 'src'),
            '@components': resolve(__dirname, 'src/components'),
            '@utils': resolve(__dirname, 'src/utils'),
            '@styles': resolve(__dirname, 'src/styles')
        }
    }
})