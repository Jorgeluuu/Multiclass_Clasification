import React from 'react';
import madridLogo from '../assets/images/madrid-logo.png';

const Footer = () => {
  const footerLinks = [
    { name: 'Contacta', href: '#' },
    { name: 'Reclamaciones y sugerencias', href: '#' },
    { name: 'Redes sociales', href: '#' },
    { name: 'Centros', href: '#' },
    { name: 'Actividades', href: '#' },
    { name: 'RSS', href: '#' },
    { name: 'Navegación', href: '#' },
    { name: 'Aviso Legal', href: '#' },
    { name: 'Mapa web', href: '#' },
    { name: 'Accesibilidad', href: '#' }
  ];

  return (
    <footer className="w-screen text-white bg-red-600 font-madrid relative left-1/2 right-1/2 -ml-[50vw] -mr-[50vw]">
      {/* Logo  */}
      <div className="border-t border-white">
        <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
          <div className="py-6">
            <div className="flex justify-center">
              <img 
                src={madridLogo} 
                alt="Comunidad de Madrid" 
                className="w-20"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Enlaces del footer */}
      <div className="border-t border-white">
        <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
          <div className="py-6">
            <div className="flex flex-wrap justify-center text-sm gap-x-6 gap-y-2">
              {footerLinks.map((link, index) => (
                <React.Fragment key={link.name}>
                  <a
                    href={link.href}
                    className="transition-colors duration-200 hover:text-red-200"
                  >
                    {link.name}
                  </a>
                  {index < footerLinks.length - 1 && (
                    <span className="hidden text-white sm:inline">|</span>
                  )}
                </React.Fragment>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Mensaje final */}
      <div className="border-t border-white">
        <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
          <div className="py-4">
          <p className="text-sm text-center">
              Proyecto educativo - Bootcamp de Inteligencia Artificial Factoría F5
              <br />
              <span className="text-xs opacity-75">
                Diseño inspirado en los portales de la Comunidad de Madrid con fines educativos únicamente
                <br />
                No está afiliado ni representa a ninguna institución oficial
              </span>
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;