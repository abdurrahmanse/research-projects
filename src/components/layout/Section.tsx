import React from 'react';
import { cn } from '@/utils/cn';

interface SectionProps {
  children: React.ReactNode;
  className?: string;
  variant?: 'default' | 'secondary';
  padding?: 'default' | 'sm' | 'lg';
  id?: string;
}

/**
 * Section Component
 * Wraps content sections with consistent styling
 */
export const Section: React.FC<SectionProps> = ({
  children,
  className,
  variant = 'default',
  padding = 'default',
  id,
}) => {
  const paddingStyles = {
    sm: 'py-8 md:py-12',
    default: 'py-12 md:py-16',
    lg: 'py-16 md:py-24',
  };

  const variantStyles = {
    default: 'bg-background',
    secondary: 'bg-muted/50 border-y border-border',
  };

  return (
    <section
      id={id}
      className={cn(
        paddingStyles[padding],
        variantStyles[variant],
        'w-full',
        className,
      )}
    >
      {children}
    </section>
  );
};

export default Section;
