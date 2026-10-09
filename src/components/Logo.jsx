import { Link } from "react-router-dom";
import logo from "../assets/logo.png";

export default function Logo() {
  return (
    <Link to="/" className="flex items-center gap-2">
      <img className="h-8 w-8 object-contain" src={logo} alt="" />
      <span className="whitespace-nowrap font-display text-lg font-bold text-navy-950">
        Bot(s) KZ
      </span>
    </Link>
  );
}