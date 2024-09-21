"use client";

import React from "react";
import {
  Navbar,
  NavbarBrand,
  NavbarMenuToggle,
  NavbarMenuItem,
  NavbarMenu,
  NavbarContent,
  NavbarItem,
  Link,
  Button,
} from "@nextui-org/react";
import { ShoppingCart, User } from "react-feather";
import { usePathname } from "next/navigation";
import { IHomePageOption } from "./interface";

const pageNavigation: IHomePageOption[] = [
  {
    name: "Products",
    link: "#",
  },
  {
    name: "Profile",
    link: "#",
  },
  {
    name: "Shop",
    link: "#",
  },
];

const pageMenu: IHomePageOption[] = [
  ...pageNavigation,
  {
    name: "Settings",
    link: "#",
  },
  {
    name: "Log In",
    link: "/login",
  },
  {
    name: "Log Out",
    link: "#",
  },
];

export default function NavigationBar() {
  const pathname = usePathname();

  return (
    <Navbar disableAnimation isBordered>
      <NavbarContent className="sm:hidden" justify="start">
        <NavbarMenuToggle />
      </NavbarContent>

      <NavbarContent className="sm:hidden pr-3" justify="center">
        <NavbarBrand>
          <p className="font-bold text-inherit">LOGO</p>
        </NavbarBrand>
      </NavbarContent>

      <NavbarContent className="hidden sm:flex gap-4" justify="center">
        <NavbarBrand>
          <p className="font-bold text-inherit">LOGO</p>
        </NavbarBrand>
        {pageNavigation.map((item, index) => {
          return (
            <NavbarItem
              isActive={pathname == item.link ? true : false}
              key={index}
            >
              <Link color="foreground" href={item.link}>
                {item.name}
              </Link>
            </NavbarItem>
          );
        })}
      </NavbarContent>

      <NavbarContent justify="end">
        <NavbarItem>
          <ShoppingCart />
        </NavbarItem>
        <NavbarItem>
          <User />
        </NavbarItem>
      </NavbarContent>

      <NavbarMenu>
        {pageMenu.map((item, index) => (
          <NavbarMenuItem key={`${item}-${index}`}>
            <Link
              className="w-full"
              color={
                index === 2
                  ? "warning"
                  : index === pageMenu.length - 1
                  ? "danger"
                  : "foreground"
              }
              href={item.link}
              size="lg"
            >
              {item.name}
            </Link>
          </NavbarMenuItem>
        ))}
      </NavbarMenu>
    </Navbar>
  );
}
