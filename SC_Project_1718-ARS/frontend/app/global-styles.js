import { injectGlobal } from 'styled-components';

/* eslint no-unused-expressions: 0 */
injectGlobal`
  html,
  body {
    height: 100%;
    width: 100%;
  }
  
  .bg-gradient-bt {
    background-image: linear-gradient(0deg, rgba(0,0,0,0.00) 0%, #2B2D42 100%);
  }
`;
