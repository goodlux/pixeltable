/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a "previous" and "next" navigation
 - create a category with a generated index page

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    {
      type: 'category',
      label: '❦ Get Started',
      items: [
        'get-started/overview',
        'get-started/installation', 
        'get-started/quickstart'
      ],
    },
    {
      type: 'category',
      label: '✦ Examples',
      items: [
        'examples/overview'
      ],
    },
    {
      type: 'category',
      label: '✧ Support',
      items: [
        'support/overview'
      ],
    },
  ],
};

export default sidebars;
