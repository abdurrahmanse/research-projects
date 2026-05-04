import React from 'react';
import { cn } from '@/utils/cn';

interface GridProps {
  children: React.ReactNode;
  className?: string;
  cols?: 1 | 2 | 3 | 4;
  gap?: 'sm' | 'default' | 'lg';
}

/**
 * Grid Component
 * Responsive grid layout helper
 */
export const Grid: React.FC<GridProps> = ({
  children,
  className,
  cols = 3,
  gap = 'default',
}) => {
  const colsStyles = {
    1: 'grid-cols-1',
    2: 'md:grid-cols-2',
    3: 'md:grid-cols-2 lg:grid-cols-3',
    4: 'md:grid-cols-2 lg:grid-cols-4',
  };

  const gapStyles = {
    sm: 'gap-4',
    default: 'gap-6',
    lg: 'gap-8',
  };

  return (
    <div
      className={cn(
        'grid grid-cols-1',
        colsStyles[cols],
        gapStyles[gap],
        className,
      )}
    >
      {children}
    </div>
  );
};

export default Grid;
