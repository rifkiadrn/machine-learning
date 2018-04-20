/**
*
* FluidLogo
*
*/

import React from 'react';
// import styled from 'styled-components';

import logoImage from 'images/logo_dark@4x.png';

class FluidLogo extends React.PureComponent { // eslint-disable-line react/prefer-stateless-function
  render() {
    return (
      <img className="img-fluid" src={logoImage} alt="Logo" />
    );
  }
}

FluidLogo.propTypes = {

};

export default FluidLogo;
