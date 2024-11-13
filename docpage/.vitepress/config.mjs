import { defineConfig } from 'vitepress'
import { set_sidebar } from './auto-sidebar.mjs'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  base:"/NCCP/",
  title: "NCCP docs",
  description: "Vitepress document site",
  themeConfig: {
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Examples', link: 'examples/markdown-examples' }
    ],

    sidebar: {
      "/examples": set_sidebar("docpage/examples")
    },

  socialLinks: [
      { icon: 'github', link: 'https://SEANPNEX/NCCP/' }
    ]
  },
  footer:{
    copyright: "Copyright@ 2024 Sean Guo",
  },
  
  search: {
    provider: "local",
    options: {
      translations: {
        button: {
          buttonText: "Search",
          buttonAriaLabel: "Search",
        },
        modal: {
          noResultsText: "No such result",
          resetButtonTitle: "Clear search",
          footer: {
            selectText: "Choose",
            navigateText: "Switch",
          },
        },
      },
    },
  },



})
