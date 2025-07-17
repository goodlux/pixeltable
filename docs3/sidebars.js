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
            'examples/pixeltable-basics',
            'examples/fundamentals/tables-and-data-operations',
            'examples/fundamentals/queries-and-expressions'
          ]
        },
        {
          type: 'category',
          label: '💡 Use Cases',
          items: [
            'examples/use-cases/rag-demo',
            'examples/use-cases/audio-transcriptions',
            'examples/object-detection-in-videos'
          ]
        },
        {
          type: 'category',
          label: '🔗 Integrations',
          items: [
            'examples/integrations/working-with-anthropic',
            'examples/integrations/working-with-openai',
            'examples/integrations/working-with-bedrock',
            'examples/integrations/working-with-hugging-face',
            'examples/integrations/working-with-ollama',
            'examples/integrations/working-with-groq',
            'examples/integrations/working-with-gemini',
            'examples/integrations/working-with-mistralai',
            'examples/integrations/working-with-deepseek',
            'examples/integrations/working-with-fireworks',
            'examples/integrations/working-with-together',
            'examples/integrations/working-with-replicate',
            'examples/integrations/working-with-llama-cpp',
            'examples/integrations/using-label-studio-with-pixeltable'
          ]
        },
        {
          type: 'category',
          label: '🛠️ Features',
          items: [
            'examples/computed-columns',
            'examples/embedding-indexes',
            'examples/feature-guides/time-zones',
            'examples/feature-guides/udfs-in-pixeltable',
            'examples/feature-guides/working-with-external-files'
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
