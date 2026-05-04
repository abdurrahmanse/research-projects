import React from 'react';
import { cn } from '@/utils/cn';

interface SectionHeaderProps {
  title: string;
  subtitle?: string;
  description?: string;
  className?: string;
}

/**
 * Section Header Component
 * Used for portfolio section headers
 */
export const SectionHeader: React.FC<SectionHeaderProps> = ({
  title,
  subtitle,
  description,
  className,
}) => {
  return (
    <div className={cn('mb-12 space-y-2', className)}>
      {subtitle && (
        <p className="text-sm font-medium text-muted-foreground uppercase tracking-wide">
          {subtitle}
        </p>
      )}
      <h2 className="text-3xl font-bold tracking-tight">{title}</h2>
      {description && (
        <p className="text-lg text-muted-foreground">{description}</p>
      )}
    </div>
  );
};

export default SectionHeader;
