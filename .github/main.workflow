workflow "Run Black" {
  on = "push"
  resolves = ["Run black"]
}

action "Run black" {
  uses = "lgeiger/black-action@master"
  args = ". --check"
}
