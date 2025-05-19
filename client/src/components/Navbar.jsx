import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import madridLogo from '../assets/images/madrid-logo.png';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isVisible, setIsVisible] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);
  const location = useLocation();

  // Control de visibilidad del navbar al hacer scroll
  useEffect(() => {
    const controlNavbar = () => {
      if (typeof window !== 'undefined') {
        if (window.scrollY > lastScrollY && window.scrollY > 100) {
          setIsVisible(false);
        } else {
          setIsVisible(true);
        }
        setLastScrollY(window.scrollY);
      }
    };

    if (typeof window !== 'undefined') {
      window.addEventListener('scroll', controlNavbar);
      return () => {
        window.removeEventListener('scroll', controlNavbar);
      };
    }
  }, [lastScrollY]);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  const navItems = [
    {
      name: 'Inicio',
      path: '/'
    },
    {
      name: 'Predicción',
      path: '/prediction'
    }
  ];

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-transform duration-300 ${
        isVisible ? 'translate-y-0' : '-translate-y-full'
      }`}
    >
      {/* Navbar principal */}
      <div className="text-white bg-red-600 font-madrid">
        <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            
            {/* Botón menú móvil  */}
            <div className="md:hidden">
              <button
                onClick={toggleMenu}
                className="inline-flex items-center justify-center p-2 text-white focus:outline-none"
                aria-expanded="false"
              >
                <span className="sr-only">Abrir menú principal</span>
                <div className="relative flex items-center justify-center w-6 h-6">
                  <span 
                    className={`absolute h-0.5 w-6 bg-white transition-all duration-300 ${
                      isMenuOpen ? 'rotate-45' : '-translate-y-1.5'
                    }`}
                  ></span>
                  <span 
                    className={`absolute h-0.5 w-6 bg-white transition-all duration-300 ${
                      isMenuOpen ? '-rotate-45' : 'translate-y-1.5'
                    }`}
                  ></span>
                </div>
              </button>
            </div>

            {/* Texto y logo*/}
            <div className="flex items-center justify-end md:justify-start md:flex-initial">
              <Link to="/" className="flex items-center cursor-pointer">
                {/* Texto solo visible en desktop */}
                <div className="hidden md:block">
                  <span className="text-2xl font-semibold">Comunidad de Madrid</span>
                </div>
                <img 
                  src={madridLogo} 
                  alt="Comunidad de Madrid" 
                  className="w-20 ml-0 md:ml-3"
                />
              </Link>
            </div>

            {/* Navegación desktop */}
            <div className="hidden md:block">
              <div className="flex items-baseline space-x-10">
                {navItems.map((item) => (
                  <Link
                    key={item.name}
                    to={item.path}
                    className={`text-white transition-all duration-200 px-3 py-2 text-lg font-medium hover:scale-105 relative ${
                      location.pathname === item.path 
                        ? 'scale-105 after:absolute after:top-12 after:left-0 after:right-0 after:h-[5px] after:bg-white' 
                        : ''
                    }`}
                    style={{ fontWeight: location.pathname === item.path ? '600' : '500' }}
                  >
                    {item.name}
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Menú móvil desplegable */}
        <div className={`md:hidden transition-all duration-300 ease-in-out ${
          isMenuOpen 
            ? 'max-h-64 opacity-100' 
            : 'max-h-0 opacity-0 overflow-hidden'
        }`}>
          <div className="bg-red-600">
            {navItems.map((item, index) => (
              <Link
                key={item.name}
                to={item.path}
                onClick={closeMenu}
                className={`block text-white text-center py-4 text-lg font-medium border-white transition-all duration-200 hover:font-semibold ${
                  index === 0 ? 'border-t border-b' : 'border-b'
                } ${
                  location.pathname === item.path ? 'font-semibold' : ''
                }`}
              >
                {item.name}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;