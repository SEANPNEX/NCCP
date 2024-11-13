import { defineConfig } from 'vitepress'
import { set_sidebar } from "../.vitepress/auto-sidebar.mjs";	// 改成自己的路径
// https://vitepress.dev/reference/site-config
export default defineConfig({
  base:"/",
  head: [["link", { rel: "icon", href: "/favicon.ico" }]],
  title: "Sean's Homepage",
  description: "A VitePress Site",
  themeConfig: {
    outlineTitle: "Outline",
    outline: [2, 6],
    // https://vitepress.dev/reference/default-theme-config
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Examples', link: '/examples/api-examples.md' }
    ],

    sidebar: { "/examples": set_sidebar("/examples") },
    aside: "left",
    socialLinks: [
      { icon: 'github', link: 'https://github.com/SEANPNEX' }
    ],
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


  },
   // 设置搜索框的样式

})
