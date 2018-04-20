/**
 *
 * Hero
 *
 */

import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import Logo from 'components/FluidLogo';

import backgroundImageFile from 'images/Inception-17.jpg';

class Hero extends React.PureComponent {
  // eslint-disable-line react/prefer-stateless-function
  render() {
    const { footer, noBottomLine, backgroundImage, hideLogo } = this.props;
    const Wrapper = styled.div`
      background: linear-gradient(rgba(43, 45, 66, 0.65), #2b2d42),
        url(${backgroundImage}) top center no-repeat;
      background-size: cover;
      padding-top: 10em;
      padding-bottom: 2em;
      ${!noBottomLine && 'border-bottom: 10px solid #E6AF2E;'};
    `;

    const StyledBody = styled.div`
      margin-bottom: 2em;
    `;

    return (
      <Wrapper className="container-fluid">
        <div className="row justify-content-center">
          <StyledBody className="col-md-8">{!hideLogo && <Logo />}</StyledBody>
        </div>
        {footer}
      </Wrapper>
    );
  }
}

Hero.propTypes = {
  footer: PropTypes.element,
  noBottomLine: PropTypes.bool,
  hideLogo: PropTypes.bool,
  backgroundImage: PropTypes.string,
};

Hero.defaultProps = {
  footer: null,
  noBottomLine: false,
  hideLogo: false,
  backgroundImage: backgroundImageFile,
};

Hero.propTypes = {};

export default Hero;
