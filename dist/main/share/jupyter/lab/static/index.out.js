/*-----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/

require('es6-promise/auto');  // polyfill Promise on IE

import {
  PageConfig
} from '@jupyterlab/coreutils';

// eslint-disable-next-line no-undef
__webpack_public_path__ = PageConfig.getOption('fullStaticUrl') + '/';

// This must be after the public path is set.
// This cannot be extracted because the public path is dynamic.
require('./imports.css');

/**
 * The main entry point for the application.
 */
function main() {
  var JupyterLab = require('@jupyterlab/application').JupyterLab;

  // Get the disabled extensions.
  var disabled = { patterns: [], matches: [] };
  var disabledExtensions = [];
  try {
    var tempDisabled = PageConfig.getOption('disabledExtensions');
    if (tempDisabled) {
      disabledExtensions = JSON.parse(tempDisabled).map(function(pattern) {
        disabled.patterns.push(pattern);
        return { raw: pattern, rule: new RegExp(pattern) };
      });
    }
  } catch (error) {
    console.warn('Unable to parse disabled extensions.', error);
  }

  // Get the deferred extensions.
  var deferred = { patterns: [], matches: [] };
  var deferredExtensions = [];
  var ignorePlugins = [];
  try {
    var tempDeferred = PageConfig.getOption('deferredExtensions');
    if (tempDeferred) {
      deferredExtensions = JSON.parse(tempDeferred).map(function(pattern) {
        deferred.patterns.push(pattern);
        return { raw: pattern, rule: new RegExp(pattern) };
      });
    }
  } catch (error) {
    console.warn('Unable to parse deferred extensions.', error);
  }

  function isDeferred(value) {
    return deferredExtensions.some(function(pattern) {
      return pattern.raw === value || pattern.rule.test(value);
    });
  }

  function isDisabled(value) {
    return disabledExtensions.some(function(pattern) {
      return pattern.raw === value || pattern.rule.test(value);
    });
  }

  var register = [];

  // Handle the registered mime extensions.
  var mimeExtensions = [];
  var extension;
  var extMod;
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/javascript-extension')) {
      disabled.matches.push('@jupyterlab/javascript-extension');
    } else {
      extMod = require('@jupyterlab/javascript-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          mimeExtensions.push(plugin);
        });
      } else {
        mimeExtensions.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/json-extension')) {
      disabled.matches.push('@jupyterlab/json-extension');
    } else {
      extMod = require('@jupyterlab/json-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          mimeExtensions.push(plugin);
        });
      } else {
        mimeExtensions.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/pdf-extension')) {
      disabled.matches.push('@jupyterlab/pdf-extension');
    } else {
      extMod = require('@jupyterlab/pdf-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          mimeExtensions.push(plugin);
        });
      } else {
        mimeExtensions.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/vega4-extension')) {
      disabled.matches.push('@jupyterlab/vega4-extension');
    } else {
      extMod = require('@jupyterlab/vega4-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          mimeExtensions.push(plugin);
        });
      } else {
        mimeExtensions.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/vega5-extension')) {
      disabled.matches.push('@jupyterlab/vega5-extension');
    } else {
      extMod = require('@jupyterlab/vega5-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          mimeExtensions.push(plugin);
        });
      } else {
        mimeExtensions.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }

  // Handled the registered standard extensions.
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/application-extension')) {
      disabled.matches.push('@jupyterlab/application-extension');
    } else {
      extMod = require('@jupyterlab/application-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/apputils-extension')) {
      disabled.matches.push('@jupyterlab/apputils-extension');
    } else {
      extMod = require('@jupyterlab/apputils-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/codemirror-extension')) {
      disabled.matches.push('@jupyterlab/codemirror-extension');
    } else {
      extMod = require('@jupyterlab/codemirror-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/completer-extension')) {
      disabled.matches.push('@jupyterlab/completer-extension');
    } else {
      extMod = require('@jupyterlab/completer-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/console-extension')) {
      disabled.matches.push('@jupyterlab/console-extension');
    } else {
      extMod = require('@jupyterlab/console-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/csvviewer-extension')) {
      disabled.matches.push('@jupyterlab/csvviewer-extension');
    } else {
      extMod = require('@jupyterlab/csvviewer-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/docmanager-extension')) {
      disabled.matches.push('@jupyterlab/docmanager-extension');
    } else {
      extMod = require('@jupyterlab/docmanager-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/documentsearch-extension')) {
      disabled.matches.push('@jupyterlab/documentsearch-extension');
    } else {
      extMod = require('@jupyterlab/documentsearch-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/extensionmanager-extension')) {
      disabled.matches.push('@jupyterlab/extensionmanager-extension');
    } else {
      extMod = require('@jupyterlab/extensionmanager-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/filebrowser-extension')) {
      disabled.matches.push('@jupyterlab/filebrowser-extension');
    } else {
      extMod = require('@jupyterlab/filebrowser-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/fileeditor-extension')) {
      disabled.matches.push('@jupyterlab/fileeditor-extension');
    } else {
      extMod = require('@jupyterlab/fileeditor-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/help-extension')) {
      disabled.matches.push('@jupyterlab/help-extension');
    } else {
      extMod = require('@jupyterlab/help-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/htmlviewer-extension')) {
      disabled.matches.push('@jupyterlab/htmlviewer-extension');
    } else {
      extMod = require('@jupyterlab/htmlviewer-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/hub-extension')) {
      disabled.matches.push('@jupyterlab/hub-extension');
    } else {
      extMod = require('@jupyterlab/hub-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/imageviewer-extension')) {
      disabled.matches.push('@jupyterlab/imageviewer-extension');
    } else {
      extMod = require('@jupyterlab/imageviewer-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/inspector-extension')) {
      disabled.matches.push('@jupyterlab/inspector-extension');
    } else {
      extMod = require('@jupyterlab/inspector-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/launcher-extension')) {
      disabled.matches.push('@jupyterlab/launcher-extension');
    } else {
      extMod = require('@jupyterlab/launcher-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/mainmenu-extension')) {
      disabled.matches.push('@jupyterlab/mainmenu-extension');
    } else {
      extMod = require('@jupyterlab/mainmenu-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/markdownviewer-extension')) {
      disabled.matches.push('@jupyterlab/markdownviewer-extension');
    } else {
      extMod = require('@jupyterlab/markdownviewer-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/mathjax2-extension')) {
      disabled.matches.push('@jupyterlab/mathjax2-extension');
    } else {
      extMod = require('@jupyterlab/mathjax2-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/notebook-extension')) {
      disabled.matches.push('@jupyterlab/notebook-extension');
    } else {
      extMod = require('@jupyterlab/notebook-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/rendermime-extension')) {
      disabled.matches.push('@jupyterlab/rendermime-extension');
    } else {
      extMod = require('@jupyterlab/rendermime-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/running-extension')) {
      disabled.matches.push('@jupyterlab/running-extension');
    } else {
      extMod = require('@jupyterlab/running-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/settingeditor-extension')) {
      disabled.matches.push('@jupyterlab/settingeditor-extension');
    } else {
      extMod = require('@jupyterlab/settingeditor-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/shortcuts-extension')) {
      disabled.matches.push('@jupyterlab/shortcuts-extension');
    } else {
      extMod = require('@jupyterlab/shortcuts-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/statusbar-extension')) {
      disabled.matches.push('@jupyterlab/statusbar-extension');
    } else {
      extMod = require('@jupyterlab/statusbar-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/tabmanager-extension')) {
      disabled.matches.push('@jupyterlab/tabmanager-extension');
    } else {
      extMod = require('@jupyterlab/tabmanager-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/terminal-extension')) {
      disabled.matches.push('@jupyterlab/terminal-extension');
    } else {
      extMod = require('@jupyterlab/terminal-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/theme-dark-extension')) {
      disabled.matches.push('@jupyterlab/theme-dark-extension');
    } else {
      extMod = require('@jupyterlab/theme-dark-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/theme-light-extension')) {
      disabled.matches.push('@jupyterlab/theme-light-extension');
    } else {
      extMod = require('@jupyterlab/theme-light-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/tooltip-extension')) {
      disabled.matches.push('@jupyterlab/tooltip-extension');
    } else {
      extMod = require('@jupyterlab/tooltip-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/ui-components-extension')) {
      disabled.matches.push('@jupyterlab/ui-components-extension');
    } else {
      extMod = require('@jupyterlab/ui-components-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }
  try {
    if (isDeferred('')) {
      deferred.matches.push('');
      ignorePlugins.push('');
    }
    if (isDisabled('@jupyterlab/vdom-extension')) {
      disabled.matches.push('@jupyterlab/vdom-extension');
    } else {
      extMod = require('@jupyterlab/vdom-extension/');
      extension = extMod.default;

      // Handle CommonJS exports.
      if (!extMod.hasOwnProperty('__esModule')) {
        extension = extMod;
      }

      if (Array.isArray(extension)) {
        extension.forEach(function(plugin) {
          if (isDeferred(plugin.id)) {
            deferred.matches.push(plugin.id);
            ignorePlugins.push(plugin.id);
          }
          if (isDisabled(plugin.id)) {
            disabled.matches.push(plugin.id);
            return;
          }
          register.push(plugin);
        });
      } else {
        register.push(extension);
      }
    }
  } catch (e) {
    console.error(e);
  }

  var lab = new JupyterLab({
    mimeExtensions: mimeExtensions,
    disabled: disabled,
    deferred: deferred
  });
  register.forEach(function(item) { lab.registerPluginModule(item); });
  lab.start({ ignorePlugins: ignorePlugins });

  // Expose global lab instance when in dev mode.
  if ((PageConfig.getOption('devMode') || '').toLowerCase() === 'true') {
    window.lab = lab;
  }

  // Handle a browser test.
  var browserTest = PageConfig.getOption('browserTest');
  if (browserTest.toLowerCase() === 'true') {
    var el = document.createElement('div');
    el.id = 'browserTest';
    document.body.appendChild(el);
    el.textContent = '[]';
    el.style.display = 'none';
    var errors = [];
    var reported = false;
    var timeout = 25000;

    var report = function() {
      if (reported) {
        return;
      }
      reported = true;
      el.className = 'completed';
    }

    window.onerror = function(msg, url, line, col, error) {
      errors.push(String(error));
      el.textContent = JSON.stringify(errors)
    };
    console.error = function(message) {
      errors.push(String(message));
      el.textContent = JSON.stringify(errors)
    };

    lab.restored
      .then(function() { report(errors); })
      .catch(function(reason) { report([`RestoreError: ${reason.message}`]); });

    // Handle failures to restore after the timeout has elapsed.
    window.setTimeout(function() { report(errors); }, timeout);
  }

}

window.addEventListener('load', main);
