import { Link, NavLink } from "react-router-dom";
import { site } from "@/data/site";
import { Button } from "@/components/ui/button";
import MobileNav from "@/components/layout/MobileNav";

export default function Header() {
  return (
    <header className="sticky top-0 z-40 border-b border-border/60 bg-background/80 backdrop-blur">
      <div className="container flex h-16 items-center justify-between">
        <Link to="/" className="font-display text-lg font-semibold">
          {site.name}
        </Link>
        <nav className="hidden items-center gap-6 text-sm font-medium md:flex">
          {site.navigation.map((item) => (
            <NavLink
              key={item.href}
              to={item.href}
              className={({ isActive }) =>
                isActive
                  ? "text-primary"
                  : "text-muted-foreground hover:text-foreground"
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="hidden items-center gap-3 md:flex">
          <Button asChild variant="outline" size="sm">
            <Link to="/program">Les programmet</Link>
          </Button>
          <Button asChild size="sm">
            <a href={site.primaryCta.href}>{site.primaryCta.label}</a>
          </Button>
        </div>
        <div className="md:hidden">
          <MobileNav />
        </div>
      </div>
    </header>
  );
}
