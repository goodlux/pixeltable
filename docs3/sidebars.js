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
  // By default, Docusaurus generates a sidebar from the filesystem, or explicitly defined here.
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
        'examples',
        {
          type: 'category',
          label: '🚀 Basics',
          items: [
            'examples2/pixeltable-basics',
            'examples2/fundamentals/tables-and-data-operations',
            'examples2/fundamentals/queries-and-expressions'
          ]
        },
        {
          type: 'category',
          label: '💡 Use Cases',
          items: [
            'examples2/use-cases/rag-demo',
            'examples2/use-cases/audio-transcriptions',
            'examples2/object-detection-in-videos'
          ]
        },
        {
          type: 'category',
          label: '🔗 Integrations',
          items: [
            'examples2/integrations/working-with-anthropic',
            'examples2/integrations/working-with-openai',
            'examples2/integrations/working-with-bedrock',
            'examples2/integrations/working-with-hugging-face',
            'examples2/integrations/working-with-ollama',
            'examples2/integrations/working-with-groq',
            'examples2/integrations/working-with-gemini',
            'examples2/integrations/working-with-mistralai',
            'examples2/integrations/working-with-deepseek',
            'examples2/integrations/working-with-fireworks',
            'examples2/integrations/working-with-together',
            'examples2/integrations/working-with-replicate',
            'examples2/integrations/working-with-llama-cpp',
            'examples2/integrations/using-label-studio-with-pixeltable'
          ]
        },
        {
          type: 'category',
          label: '🛠️ Features',
          items: [
            'examples2/computed-columns',
            'examples2/embedding-indexes',
            'examples2/feature-guides/time-zones',
            'examples2/feature-guides/udfs-in-pixeltable',
            'examples2/feature-guides/working-with-external-files'
          ]
        }
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
  
  // SDK Reference sidebar
  sdkSidebar: [
    'sdk/index',
    {
      type: 'category',
      label: 'Core API',
      items: [
        'sdk/core/index',
        'sdk/core/core'
      ],
    },
    {
      type: 'category',
      label: 'Functions',
      items: [
        'sdk/functions/index',
        'sdk/functions/functions',
        'sdk/functions/functions-anthropic',
        'sdk/functions/functions-audio',
        'sdk/functions/functions-bedrock',
        'sdk/functions/functions-date',
        'sdk/functions/functions-image',
        'sdk/functions/functions-math',
        'sdk/functions/functions-openai',
        'sdk/functions/functions-video'
      ],
    },
    {
      type: 'category',
      label: 'Input/Output',
      items: [
        'sdk/io/index',
        'sdk/io/io'
      ],
    },
    {
      type: 'category',
      label: 'Iterators',
      items: [
        'sdk/iterators/index',
        'sdk/iterators/iterators'
      ],
    },
    {
      type: 'category',
      label: 'Extensions',
      items: [
        'sdk/ext/index',
        'sdk/ext/ext',
        'sdk/ext/ext-functions',
        'sdk/ext/ext-functions-whisperx',
        'sdk/ext/ext-functions-yolox'
      ],
    }
  ],
};

export default sidebars;
