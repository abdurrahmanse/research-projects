import React from 'react';
import { cn } from '@/utils/cn';

interface ContainerProps {
  children: React.ReactNode;
  className?: string;
  size?: 'default' | 'sm' | 'lg';
}

/**
 * Container Component
 * Provides consistent max-width and padding
 */
export const Container: React.FC<ContainerProps> = ({
  children,
  className,
  size = 'default',
}) => {
  const sizeStyles = {
    sm: 'max-w-2xl',
    default: 'max-w-6xl',
    lg: 'max-w-7xl',
  };

  return (
    <div className={cn(
      'mx-auto px-4 sm:px-6 lg:px-8 w-full',
      sizeStyles[size],
      className,
    )}>
      {children}
    </div>
  );
};

export default Container;
