import React from 'react';
import PropTypes from 'prop-types';
import Navbar from 'components/Navbar';
import Footer from 'components/Footer';

const Layout = (props) => {
  return (
    <div>
      <Navbar />
      {props.children}
      <Footer />
    </div>
  );
};

Layout.propTypes = {
  children: PropTypes.element,
};

export default Layout;
