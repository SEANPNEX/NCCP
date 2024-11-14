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
      { text: 'Examples', link: 'docs/examples/markdown-examples' },
      { text: 'Map', link: "docs/map/map_docs"},
      { text: 'Database', link: 'docs/db/db_docs'},
    ],

  sidebar: set_sidebar("docpage/docs"),

  socialLinks: [
      { icon: 'github', link: 'https://github.com/SEANPNEX/NCCP/' }
    ]
  },
  footer:{
    copyright: "Copyright@ 2024 NCCP",
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
