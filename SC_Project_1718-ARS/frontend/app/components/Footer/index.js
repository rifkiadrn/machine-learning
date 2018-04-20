/**
*
* Footer
*
*/

import React from 'react';
import styled from 'styled-components';


class Footer extends React.PureComponent { // eslint-disable-line react/prefer-stateless-function
  render() {
    const StyledDiv = styled.div`
      background-color: #2B2D42;
      color: white;
      padding-top: 1em;
      padding-bottom: 1em;
    `;
    return (
      <StyledDiv className="container-fluid">
        MOVING - Your Trusted Movie Rating
      </StyledDiv>
    );
  }
}

Footer.propTypes = {

};

export default Footer;
